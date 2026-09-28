import os
import html
import time
import pytest
from utils.helpers import get_driver, take_screenshot, SCREENSHOT_DIR, REPORT_DIR

results = []
start_time = time.time()


def pytest_sessionstart(session):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)
    for file in os.listdir(SCREENSHOT_DIR):
        if file.endswith(".png"):
            os.remove(os.path.join(SCREENSHOT_DIR, file))


@pytest.fixture(scope="module")
def driver():
    d = get_driver()
    yield d
    d.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" or (report.when == "setup" and report.failed):
        error = ""
        if call.excinfo is not None:
            error = str(call.excinfo.value)[:300]

        if report.failed and "driver" in item.funcargs:
            try:
                take_screenshot(item.funcargs["driver"], "FAILED_" + item.name)
            except Exception:
                pass

        results.append({
            "name": item.name,
            "result": report.outcome.upper(),
            "time": round(report.duration, 2),
            "error": error,
        })


def pytest_sessionfinish(session, exitstatus):
    passed = 0
    failed = 0
    for r in results:
        if r["result"] == "PASSED":
            passed = passed + 1
        else:
            failed = failed + 1

    page = "<html>\n<head><title>Test Report</title></head>\n<body>\n"
    page += "<h1>Test Report</h1>\n"
    page += "<p>Tested by: Arunavo</p>\n"
    page += "<p>Date: " + time.strftime("%d-%m-%Y %H:%M:%S") + "</p>\n"
    page += "<p>Total: " + str(len(results)) + " | Passed: " + str(passed) + " | Failed: " + str(failed) + "</p>\n"
    page += "<p>Total time: " + str(round(time.time() - start_time, 2)) + " seconds</p>\n"

    page += "<table border='1'>\n"
    page += "<tr><td>No</td><td>Test Name</td><td>Result</td><td>Time (sec)</td><td>Error</td></tr>\n"
    number = 1
    for r in results:
        page += "<tr><td>" + str(number) + "</td><td>" + r["name"] + "</td><td>" + r["result"] + "</td><td>" + str(r["time"]) + "</td><td>" + html.escape(r["error"]) + "</td></tr>\n"
        number = number + 1
    page += "</table>\n"

    page += "<h3>Screenshots</h3>\n"
    for file in sorted(os.listdir(SCREENSHOT_DIR)):
        if file.endswith(".png"):
            page += "<a href='../screenshots/" + file + "'>" + file + "</a><br>\n"

    page += "</body>\n</html>"

    with open(os.path.join(REPORT_DIR, "report.html"), "w") as f:
        f.write(page)
    print("\nReport saved: reports/report.html")
