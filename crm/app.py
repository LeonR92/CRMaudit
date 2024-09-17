from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from crm.database.db import BDVersicherungsunternehmen, session

crm = Blueprint("crm", __name__, template_folder="templates", static_folder="static")


@crm.route("/customers")
def customers():
    return render_template("index.html")


@crm.route("/add_company", methods=["POST"])
def add_company():
    mandantkuerzel = request.form.get('mandantkuerzel')
    mandantenname = request.form.get('mandantenname')
    parent_name = request.form.get('parent_name')

    # Use class method to add company
    BDVersicherungsunternehmen.add_company(session, mandantkuerzel, mandantenname, parent_name)
    
    # Redirect to a new route (e.g., /company/<id>)
    return redirect(url_for('crm.customers'))

@crm.route("/update_company", methods=["GET"])
def update_company_form():
    companies = session.query(BDVersicherungsunternehmen).all()  # Get all companies for dropdown
    return render_template("update.html", companies=companies)


@crm.route("/update_company", methods=["POST"])
def update_company():
    company_id = request.form.get('company_id')
    mandantkuerzel = request.form.get('mandantkuerzel')
    mandantenname = request.form.get('mandantenname')
    parent_name = request.form.get('parent_company')

    # Get company to update
    company = session.query(BDVersicherungsunternehmen).get(company_id)

    # Update fields
    company.mandantkuerzel = mandantkuerzel
    company.mandantenname = mandantenname
    if parent_name:
        parent = session.query(BDVersicherungsunternehmen).filter_by(mandantenname=parent_name).first()
        company.parent_id = parent.id if parent else None

    # Commit changes
    session.commit()

    return redirect(url_for('crm.customers'))
