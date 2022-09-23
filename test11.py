import test_sql
filename="sql1.xlsx"


test_sql = test_sql.test_sql
filename = "./result/"+filename
result1=test_sql.test_file(filename)
print("test11:"+filename)
test_sql.out_file_excel(filename,result1)