from flask import Flask, render_template, request, url_for, redirect
from salary import salary_and_qol
from topunis import top_unis

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        province_ = request.form["provinces"]
        job_ = request.form["jobs"]

        return redirect(url_for("output", province = province_, job = job_))
    else:
        return render_template("index.html")

@app.route("/<province>?<job>")
def output(province, job):
    #return f"<h1>{job} and {province}</h1>"
    topNum = 10
    [sal, qol] = salary_and_qol(province, job)
    [uni_names_, dom_tuition_, inter_tuition_] = top_unis(province, topNum)
    print(uni_names_)
    return render_template('results.html',
    province = province,
    job = job,
    sal = sal,
    qol = qol,
    uni_names = uni_names_,
    dom_tuition = dom_tuition_,
    inter_tuition = inter_tuition_,
    top_num = topNum
    )

if __name__ == "__main__":
    app.run(debug=True)