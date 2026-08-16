import pandas as pd 

file_path = "data/input/Online Retail.csv"

df = pd.read_csv(file_path)

print(df.head())

# print(df.shape)

# print(df.columns.tolist())

# print(df.dtypes)

# print(df.isnull().sum())

# print(df.duplicated().sum())

# cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

# sales = df[~cancelled]

# print(len(sales))

# print(cancelled.sum())

# print(len(df.fillna({"CustomerID": "Unknown"}).query("UnitPrice <= 0")))

# print(df.query("Quantity <= 0").head(10))
# print(len(df.query("Quantity <= 0").head(10)))

# print(df["Quantity"].isnull().sum())
# print(df["CustomerID"].isnull().sum())
# print(df["Country"].isnull().sum())
# print(df["InvoiceNo"].isnull().sum())
# print(df["StockCode"].isnull().sum())
# print(df["Description"].isnull().sum())
# print(df["InvoiceDate"].isnull().sum())

# print()
# print(df[df["CustomerID"].isnull()]["Description"].isnull().sum())

print((~df["StockCode"].astype(str).str.match(r".*[A-Z]")).sum())

