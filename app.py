from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])

def quiz():
    citizen = request.form['citizen'] == 'yes'
    legal = request.form['legal'] == 'yes'
    benefit = request.form['benefit'] == 'no'
    owned = request.form['owned'] == 'no'
    special = request.form['special'] == 'yes'
    homeless = request.form['homeless'] == 'yes'

    if not (citizen and legal and benefit and owned):
        if homeless:
            result = "You may qualify for Emergency Housing if you’re facing imminent homelessness."
        else:
            result = ("You may qualify for UISP if you’re upgrading an existing informal settlement. Otherwise, "
                      "you do not qualify for any government housing programme.")
        return render_template('results.html', result=result)

    if not homeless:
        living = request.form['living']
        income = request.form['income']
    else:
        living = None
        income = None

    result = determine_housing_options(citizen, legal, benefit, owned, special, homeless, living, income)
    return render_template('results.html', result=result)

def determine_housing_options(citizen, legal, benefit, owned, special, homeless, living, income):
    if homeless:
        return "Emergency Housing Programme/Transitional housing"
    else:
        if living == "informal":
            if income == "R0 - R1850":
                return ("You may qualify for Community Residential Units, Individual Housing Subsidy, Breaking New "
                        "Ground, Inclusionary housing, UISP or ePHP programmes.")
            elif income == "R1851 - R3500":
                return ("You may qualify for the individual housing subsidy, Social Housing, Inclusionary housing, "
                        "UISP or ePHP programmes")
            elif income == "R3501 - R22000":
                return ("You may qualify for Social Housing, Inclusionary housing, or the First Home Finance "
                        "programmes. In practice you may also qualify for UISP.")
            else:
                return ("You may qualify for inclusionary housing in some places. In practice you may also qualify for "
                        "UISP.")
        else:
            if income == "R0 - R1850":
                return ("You may qualify for Community Residential Units, Individual Housing Subsidy, Breaking New "
                        "Ground or Inclusionary housing programmes.")
            elif income == "R1851 - R3500":
                return ("You may qualify for the Individual Housing Subsidy, Social Housing, Breaking New Ground or "
                        "the Inclusionary housing programmes.")
            elif income == "R3501 - R22000":
                return "You may qualify for Social Housing, Inclusionary housing, or the First Home Finance programmes."
            else:
                return ("You may qualify for inclusionary housing in some places, depending on the specific income "
                        "criteria set by local authorities.")


if __name__ == '__main__':
    app.run()
