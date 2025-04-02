from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fpdf import FPDF
import time

# Setup headless Chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")  # run in background
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

# Load the page
url = "https://www.studocu.com/in/document/apj-abdul-kalam-technological-university/data-mining-and-ware-housing/dm-3-data-mining-notes/65297106"
driver.get(url)

# Wait for JavaScript to load the content
time.sleep(5)  # adjust depending on your internet speed

# Get full rendered text
text = driver.find_element("tag name", "body").text

# Close browser
driver.quit()

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for line in text.split('\n'):
    if line.strip():
        pdf.multi_cell(0, 10, line.strip())

pdf.output("scraped_studocu.pdf")

print("✅ PDF saved as scraped_studocu.pdf")
