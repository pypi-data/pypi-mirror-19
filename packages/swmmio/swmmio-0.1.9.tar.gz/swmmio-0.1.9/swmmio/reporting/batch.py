from swmmio.swmmio import Model
from swmmio.reporting import reporting
from swmmio.reporting import functions
from swmmio.utils import swmm_utils as su
from time import strftime
import os
import shutil
import math
from itertools import chain

REPORT_DIR_NAME = 'Report'

def batch_cost_estimates(baseline_dir, segments_dir, options_dir, results_file,
                         supplemental_cost_data=None, create_proj_reports=True):
    """
    compute the cost estimate of each model/option in the segments and
    combinations directories. Resulsts will be printed in the results text file.
    """
    #combine the segments and options (combinations) into one iterable
    paths = (segments_dir, options_dir)
    baseline = Model(baseline_dir)

    for path, dirs, files in chain.from_iterable(os.walk(path) for path in paths):

        for f in files:
            if '.inp' in f:
                inp_path = os.path.join(path,f)
                alt = Model(inp_path)

                #calculate the cost
                costsdf = functions.estimate_cost_of_new_conduits(baseline, alt,
                                                                  supplemental_cost_data)
                cost_estimate = costsdf.TotalCostEstimate.sum() / math.pow(10, 6)
                print '{}: ${}M'.format(alt.name, round(cost_estimate,1))

                model_id = os.path.splitext(f)[0]
                with open(results_file, 'a') as res:
                    res.write('{}, {}\n'.format(model_id, cost_estimate))

                if create_proj_reports:
                    #create a option-specific per segment costing csv file
                    report_dir = os.path.join(alt.inp.dir, REPORT_DIR_NAME)
                    fname = '{}_CostEstimate_{}.csv'.format(alt.name, strftime("%y%m%d"))
                    cost_report_path = os.path.join(report_dir, fname)
                    if not os.path.exists(report_dir):os.mkdir(report_dir)
                    costsdf.to_csv(cost_report_path)


def batch_post_process(options_dir, baseline_dir, log_dir, bbox=None, overwrite=False):
    """
    batch process all models in a given directory, where child directories
    each model (with .inp and .rpt companions). A bbox should be passed to
    control where the grahics are focused. Specify whether reporting content
    should be overwritten if found.
    """
    baseline = Model(baseline_dir)
    folders = os.listdir(options_dir)
    logfile = os.path.join(log_dir, 'logfile.txt')
    with open (logfile, 'a') as f:
        f.write('MODEL,NEW_SEWER_MILES,IMPROVED,ELIMINATED,WORSE,NEW\n')
    for folder in folders:
        #first check if there is already a Report directory and skip if required
        current_dir = os.path.join(options_dir, folder)
        report_dir = os.path.join(current_dir, REPORT_DIR_NAME)
        if not overwrite and os.path.exists(report_dir):
            print 'skipping {}'.format(folder)
            continue

        else:
            #generate the report
            current_model = Model(current_dir)
            print 'Generating report for {}'.format(current_model.inp.name)
            #reporting.generate_figures(baseline, current_model, bbox=bbox, imgDir=report_dir, verbose=True)
            report = reporting.Report(baseline, current_model)
            report.write(report_dir)

            #keep a summay log
            with open (logfile, 'a') as f:
                #'MODEL,NEW_SEWER_MILES,IMPROVED,ELIMINATED,WORSE,NEW'
                f.write('{},{},{},{},{},{}\n'.format(
                                                    current_model.inp.name,
                                                    report.sewer_miles_new,
                                                    report.parcels_flooding_improved,
                                                    report.parcels_eliminated_flooding,
                                                    report.parcels_worse_flooding,
                                                    report.parcels_new_flooding
                                                    )
                                                )

def gather_files_in_dirs(rootdir, targetdir, searchfilename, newfilesuffix='_Impact.png'):

    """
    scan through a directory and copy files having a given file name into a
    taget directory. This is useful when wanting to collect the same report image
    within a SWMM model's Report directory (when there are many models).

    This expects the Parent<Parent directory of a file to be called the unique
    model ID. For example, the png in the following dir:

        rootdir > ... > M01_R01_W02 > Report > '03 Impact of Option.png'

    would be copied as follows:

        targetdir > 'M01_R01_W02_Impact.png'

    """


    for root, dirs, files in os.walk(rootdir):

        for f in files:
            #if the file name = the searched file name, copy it to the target dirs
            #for example searchfilename = '03 Impact of Option.png'
            if os.path.basename(f) == searchfilename:
                current_dir = os.path.dirname(os.path.join(root, f))
                model_id = os.path.basename(os.path.dirname(current_dir))

                newf = os.path.join(targetdir, model_id + newfilesuffix)
                shutil.copyfile(os.path.join(root, f), newf)
