import mechanize
import datetime,os


def calculateoneweek( filename, dateref):
    url = "http://www.abc"+"bourse.com/download/historiques.aspx?f=ex"
    br = mechanize.Browser()
    br.set_handle_robots(False) # ignore robots
    br.open(url)
    br.select_form(name="aspnetForm")
    br.form.find_control(name='ctl00$BodyABC$eurolist').items[0].selected=True


    firstDate=dateref.strftime('%d/%b/%Y')
    secondDate=(dateref+ datetime.timedelta(days=-7)).strftime('%d/%b/%Y')

    br["ctl00$BodyABC$strDateDeb"]=secondDate
    br["ctl00$BodyABC$strDateFin"]=firstDate
    res = br.submit()

    content = res.read()

    with open(filename, "a") as f:
        f.write(content)

filename="complete.csv"
try:
    os.remove(filename)
except OSError:
    pass

dateref=datetime.datetime.now()
for x in range(0, 1404):
    calculateoneweek("complete.csv",dateref)
    dateref=dateref+ datetime.timedelta(days=-7)
    print dateref
