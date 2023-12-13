#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import json
from rpt_dosi.helpers import find_closest_match
import pkg_resources
from path import Path


def guess_phantom_id(phantom_name):
    # which phantom ?
    phantoms = {"ICRP 110 AF": "1", "ICRP 110 AM": "2"}
    phantom_name = find_closest_match(phantom_name, phantoms.keys())
    phantom_id = phantoms[phantom_name]
    return phantom_id, phantom_name


def guess_source_id(phantom_name, source_name):
    sources_file = get_data_folder(phantom_name) / "opendose_sources.json"
    with open(sources_file) as f:
        sources = json.load(f)
    return get_match_in_list(sources, source_name)


def guess_isotope_id(phantom_name, isotope_name):
    isotopes_file = get_data_folder(phantom_name) / "opendose_isotopes.json"
    with open(isotopes_file) as f:
        isotopes = json.load(f)
    return get_match_in_list(isotopes, isotope_name)


def get_data_folder(phantom_name):
    _, phantom_name = guess_phantom_id(phantom_name)
    folder = phantom_name.replace(" ", "_")
    folder = pkg_resources.resource_filename("rpt_dosi", f"data/{folder}")
    return Path(folder)


def get_svalue_data_filename(phantom_name, source_name, isotope_name):
    output = (
        get_data_folder(phantom_name) / f"{isotope_name}_{source_name}.json".lower()
    )
    return output


def get_match_in_list(names_list, name):
    rnames_list = {list(d.values())[0]: list(d.keys())[0] for d in names_list}
    values = list(rnames_list.keys())
    name = find_closest_match(name, values)
    return rnames_list[name], name


def web_svalues_get_driver():
    # Define the URL of the form
    url = "https://opendose.org/svalues"

    # Set up a headless browser
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # Open the form URL
    driver.get(url)

    # Select the phantom model in the dropdown with explicit wait
    model_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phantom"))
    )
    return driver, model_dropdown


def web_svalues_select_phantom(driver, model_dropdown, phantom_id):
    # which phantom ?
    model_dropdown_select = Select(model_dropdown)
    model_dropdown_select.select_by_value(phantom_id)

    # Wait for the submit button to be clickable
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "submit")))
    form = driver.find_element(By.ID, "myform")
    form.submit()

    # Wait for the source dropdown to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "source")))


def get_all_dropdown_options(driver, name):
    # Find the 'name' dropdown element
    dropdown = driver.find_element(By.ID, name)

    # Get all options from the dropdown
    options = dropdown.find_elements(By.TAG_NAME, "option")

    # Extract the values from the options
    source_attributes = [
        {option.get_attribute("value"): option.text}
        for option in options
        if "Select a " not in option.text
    ]

    return source_attributes


def web_svalues_query_data(driver, source_id, isotope_id):
    # Select values for source and isotope, then click submit
    source_dropdown = driver.find_element(By.ID, "source")
    source_dropdown_select = Select(source_dropdown)
    source_dropdown_select.select_by_value(source_id)  # 264 = liver

    isotope_dropdown = driver.find_element(By.ID, "isotope")
    isotope_dropdown_select = Select(isotope_dropdown)
    isotope_dropdown_select.select_by_value(isotope_id)  # 575 = Lu177

    # Submit the form
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "submit")))
    form = driver.find_element(By.ID, "myform")
    form.submit()

    # Wait for the page to load and the download button to be present
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "div_table"))
    )
    table = driver.find_element(By.ID, "div_table")

    # Get the HTML content of the table
    table_html = table.get_attribute("outerHTML")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(table_html, "html.parser")

    # Extract data from the table
    data = []
    for row in soup.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        row_data = [col.get_text(strip=True) for col in cols]
        data.append(row_data)

    return data


def get_svalue_and_mass(phantom, roi, rad, dest_roi):
    _, source_name = guess_source_id(phantom, roi)
    _, rad_name = guess_isotope_id(phantom, rad)
    file_name = get_svalue_data_filename(phantom, source_name, rad_name)
    with open(file_name, "r") as f:
        data = json.load(f)
    _, r = guess_source_id(phantom, dest_roi)
    print("dest roi is", r)
    print(data)
    print()
    d = data.find(dest_roi)
    print(d)

    return 1.3713e-5, 1
