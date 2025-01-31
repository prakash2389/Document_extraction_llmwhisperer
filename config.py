# Define default key pairs and descriptions
DEFAULT_KEYPAIRS = """
CURRENCY
INVOICE_AMOUNT
TOTAL_OTHER_CHARGES
INVOICE_DATE
MAIN_HSN_CODE
PO_NUMBER
INVOICE_NUMBER
IRN_NUMBER
EXTENDED_PRICE
MATERIAL_DESCRIPTION
MATERIAL_NUMBER
PO_NUMBER
PO_LINE
QTY_FROM_INVOICE
UNIT_PRICE
HSN_SAC_CODE
BILL_TO_NAME
SHIP_TO_PLANT_GSTIN
SHIP_TO_PLANT_ADDRESS
SHIP_TO_PLANT_ZIP_CODE
SHIP_TO_PLANT_NAME
TOTAL_CGST_AMOUNT
TOTAL_IGST_AMOUNT
TOTAL_SGST_AMOUNT
TOTAL_UTGST_AMOUNT
TOTAL_TAX_AMT
VENDOR_ADDRESS
VENDOR_NAME
VENDOR_PAN_NUMBER
VENDOR_GSTIN_NUMBER
VENDOR_ZIPCODE
"""

DEFAULT_FIELD_DESCRIPTIONS = """
CURRENCY: Look for any currency symbols (₹, $, €, etc.) or currency codes (INR, USD, EUR, etc.) in the document. If not explicitly mentioned, use 'INR' as the default for Indian invoices.
INVOICE_AMOUNT: Total amount mentioned in the invoice, including taxes.
TOTAL_OTHER_CHARGES: Any other charges like shipping, handling, etc.
INVOICE_DATE: The date when the invoice was issued.
MAIN_HSN_CODE: The main HSN or SAC CODE for the products or services. If not explicitly found, look for HSN/SAC Code and use this.
PO_NUMBER: Purchase order number associated with the invoice.
INVOICE_NUMBER: The unique invoice number issued by the vendor.
IRN_NUMBER: The Invoice Reference Number.
EXTENDED_PRICE: The total price for the products/services before taxes. If not explicitly found, calculate by multiplying Rate per unit by Qty.
MATERIAL_DESCRIPTION: A detailed description of the materials in the invoice.
MATERIAL_NUMBER: The unique material number for the items in the invoice.
PO_NUMBER: The number associated with the purchase order line items.
PO_LINE: The line item number of the purchase order.
QTY_FROM_INVOICE: Quantity of items listed in the invoice.
UNIT_PRICE: Price per unit of the item, without taxes. If not explicitly found, use Rate per unit or Fixed cost per truck.
HSN_SAC_CODE: HSN or SAC code for the product or service. If not explicitly found, look for HSN/SAC Code and use this.
BILL_TO_NAME: Name of the Buyer entity receiving the goods or services or Recipient. If not found, use Consigner/Bill To Address
SHIP_TO_PLANT_GSTIN: GSTIN NO. of the buyer or Recipient or Consigner/Bill To-. If not explicitly found, Use GSTIN NO. of BILL_TO_NAME field.
SHIP_TO_PLANT_ADDRESS: Extract the shipping plant's address. If not explicitly found, use the BILL_TO_NAME field as a fallback to infer the plant's address.
SHIP_TO_PLANT_ZIP_CODE: Look for a 6-digit number in the SHIP_TO_PLANT_ADDRESS. Search for patterns like: \d{6}, -\d{6}, or (\d{6}). If found, extract only the 6 digits.
SHIP_TO_PLANT_NAME: Use exactly the same value as BILL_TO_NAME. These fields should always match as they refer to the same entity.
TOTAL_CGST_AMOUNT: The total CGST (Central Goods and Services Tax) amount.
TOTAL_IGST_AMOUNT: The total IGST (Integrated Goods and Services Tax) amount.
TOTAL_SGST_AMOUNT: The total SGST (State Goods and Services Tax) amount.
TOTAL_UTGST_AMOUNT: The total UTGST (Union Territory Goods and Services Tax) amount.
TOTAL_TAX_AMT: Calculate TOTAL_TAX_AMT as the sum of the available values for TOTAL_CGST_AMOUNT, TOTAL_SGST_AMOUNT, TOTAL_IGST_AMOUNT, and TOTAL_UTGST_AMOUNT. If a component is 'Not found', exclude it from the calculation. If all components are 'Not found', return 'Not found'.
VENDOR_ADDRESS: Full address of the vendor or supplier.
VENDOR_NAME: If the vendor name is explicitly mentioned, extract it. If not, derive the name from the vendor's address if possible. For example, look for patterns like "Regd. Transporter of [Name]" or other indicators in the vendor's address.
VENDOR_GSTIN_NUMBER: GSTIN of the vendor or supplier.
VENDOR_PAN_NUMBER: This should be derived from the VENDOR_GSTIN_NUMBER. Remove the first two characters and the last character from the GSTIN of Vendor to get the PAN number. For example, if GSTIN is 29AAACM5132A1ZZ, the PAN would be AAACM5132A.
VENDOR_ZIPCODE: Look for a 6-digit number in the VENDOR_ADDRESS. Search for patterns like: \d{6}, -\d{6}, )\d{6} or (\d{6}). If found, extract only the 6 digits.
"""
