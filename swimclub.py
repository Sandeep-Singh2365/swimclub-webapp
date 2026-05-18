import statistics
import hfpy_utils

from pathlib import Path

# FOLDER = 'swimdata/'
# CHARTS = "charts/"
BASE_DIR = Path(__file__).resolve().parent
FOLDER = BASE_DIR / "swimdata"
CHARTS = BASE_DIR / "charts"



def read_swim_data(filename):
    """Return swim date from a file

    Given the name of a swimmer's file (in filename), extract all the required data,
    then return it to caller as a tuple.

    Docstring for read_swim_data
    """
    swimmer, age, distance, stroke = filename.removesuffix('.txt').split('-')
    # with open(FOLDER+filename) as file:
    with open(FOLDER/filename) as file:
        lines = file.readlines()
        times = lines[0].strip().split(',')
    converts = []
    for t in times:
        # The minutes value might be missing, so guard against this causing a crash
        if ':' in t:
            minutes, rest = t.split(':')
            seconds, hundreths = rest.split('.')
            converted_time = (int(minutes)*60*100) + (int(seconds)*100) + (int(hundreths))
        else:
            minutes = 0
            seconds, hundreths = t.split('.')
            converted_time = (int(seconds)*100) + int(hundreths)
        converts.append(converted_time)
    average = statistics.mean(converts)
    # mins_secs, hundreths = str(round(average/100,2)).split('.')
    mins_secs, hundreths = f"{(average/100):.2f}".split('.')
    mins_secs = int(mins_secs)
    minutes = mins_secs//60
    seconds = mins_secs - (minutes*60)
    # average = str(minutes) + ':' + str(seconds) + '.' + str(hundreths)
    # average = f"{minutes}:{seconds}.{hundreths}"
    average = f"{minutes}:{seconds:0>2}.{hundreths}"

    # return swimmer, age, distance, stroke, times, average
    return swimmer, age, distance, stroke, times, average, converts
        


# def produce_bar_charts(fn):
def produce_bar_charts(fn, location = CHARTS):
    """ Given the name of swimmer's file, produce a HTML/SVG-based bar chart.

    Save the charts to CHARTS folder. Return the path to bar chart file.

    Docstring for produce_bar_charts
    
    :param fn: Description
    """
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(fn)
    from_max = max(converts)
    svgs = ""
    times.reverse()
    converts.reverse()

    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    header = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
            <link rel="stylesheet" href="/static/webapp.css">
        </head>
        <body>
            <h3>{title}</h3>
    """
    body = ""
    for n,t in enumerate(times):
        # print(converts[n])
        # bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 400)
        # print(bar_width)
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body = body+ f"""
        <svg height="30" width="400">
                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
        </svg>{t}<br />
        """
    footer = f"""
        <p>Average time: {average}</p>
        </body>
    </html>
    """

    page = header + body + footer

    # save_to = f"charts/{fn.removesuffix('.txt')}.html"
    # save_to = f"{CHARTS}{fn.removesuffix('.txt')}.html"
    if location != CHARTS:
        location = BASE_DIR / location
    save_to = f"{location}/{fn.removesuffix('.txt')}.html"
    with open(save_to, "w") as sf:
        print(page, file=sf)

    return save_to

