#coding:utf-8
import cgi

print("Content-type:text/html; charset=utf-8\n")

html="""<!DOCTYPE html>
<head>
<title>Form</title>
</head>
<body>
<form action="form.py" method="post">
<input type="text" name="name" value=""/>
<input type="submit" value="Submit"/>
</form>
</body>
</html>
"""