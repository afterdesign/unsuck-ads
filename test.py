# -*- coding:utf-8 -*-

import sys
import time
import psutil
from tabulate import tabulate
from selenium import webdriver
from termcolor import cprint


def run_chrome(extensions):
    """
    Run browser
    """
    chromeoptions = webdriver.ChromeOptions()
    for extension in extensions:
        chromeoptions.add_extension(
            "extensions/{extension}".format(
                extension=extension
            )
        )

    capabilities = webdriver.common.desired_capabilities.DesiredCapabilities.CHROME.copy()
    capabilities.update(chromeoptions.to_capabilities())

    browser = webdriver.Chrome(
        desired_capabilities=capabilities
    )

    browser.set_window_position(0, 0)
    browser.set_window_size(1920, 1080)

    while len(browser.window_handles) > 1:
        browser.switch_to_window(browser.window_handles[0])
        browser.close()

    browser.switch_to_window(browser.window_handles[0])

    return browser


def count_chrome_memory(pid):
    """
    Get memory from all chrome helpers and subprocessess
    """

    chrome_pid = psutil.Process(pid).children()[0].pid

    process = psutil.Process(chrome_pid)
    memory_info = process.memory_info()[0]

    for single in process.children():
        memory_info += single.memory_info()[0]

    return memory_info


def get_memory_stats(browser, url):
    """
    Go to page, scroll thorugh it and get informations about memory usage.
    """
    memory_info = {}

    # get memory after browser starts
    memory_info['start'] = count_chrome_memory(browser.service.process.pid)

    # Open URL
    browser.get(url)

    # Scroll through page and wait for additional content to load
    for scroll in [round(x * 0.2, 2) for x in range(1, 6)]:
        browser.execute_script(
            "window.scrollTo(0, {scroll} * document.body.scrollHeight);".format(
                scroll=scroll
            )
        )
        time.sleep(5)

    # Get memory after scrolling
    memory_info['stop'] = count_chrome_memory(browser.service.process.pid)

    # close and quit to start fresh
    browser.close()
    browser.quit()

    return memory_info


def main():
    """
    Run benchmark
    """

    browser_with_blockers = run_chrome(
        ['ublock.crx', 'ghostery.crx']
    )

    memory_stats_with_blockers = get_memory_stats(
        browser_with_blockers,
        sys.argv[1]
    )

    browser_without_blockers = browser_with_blockers = run_chrome([])
    memory_stats_without_blockers = get_memory_stats(browser_without_blockers, sys.argv[1])

    table_to_print = tabulate(
        [
            [
                "with adblockers",
                (memory_stats_with_blockers['stop'] - memory_stats_with_blockers['start']) / float(2**20)
            ],
            [
                "without adblockers",
                (memory_stats_without_blockers['stop'] - memory_stats_without_blockers['start']) / float(2**20)
            ]
        ],
        tablefmt="grid"
    )

    cprint(table_to_print, 'green', 'on_red', attrs=['bold'])

if __name__ == '__main__':
    main()
