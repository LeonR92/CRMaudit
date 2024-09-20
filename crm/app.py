from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from crm.database.db import BDVersicherungsunternehmen, session,Kontaktperson
from sqlalchemy.orm import aliased
import time



crm = Blueprint("crm", __name__, template_folder="templates", static_folder="static")



@crm.route("/", methods=["GET"])
def index():
    # Start the timer at the beginning of the request
    start_time = time.time()

    # Self-join to handle parent and subsidiaries
    parent = aliased(BDVersicherungsunternehmen)
    subsidiary = aliased(BDVersicherungsunternehmen)

    # Explicit join to Kontaktperson table
    query = (
        session.query(
            parent.id.label("parent_id"),
            parent.mandantenname.label("parent_name"),
            subsidiary.id.label("subsidiary_id"),
            subsidiary.mandantenname.label("subsidiary_name"),
            Kontaktperson.name.label("kontaktperson_name"),
            Kontaktperson.email.label("kontaktperson_email"),
            Kontaktperson.phone.label("kontaktperson_phone")
        )
        # Self-join to get parent-subsidiary relationship
        .outerjoin(subsidiary, subsidiary.parent_id == parent.id)
        # Join with Kontaktperson table
        .outerjoin(Kontaktperson, Kontaktperson.versicherungsunternehmen_id == subsidiary.id)
    )

    # Execute the query
    result = query.all()

    # Stop the timer just before rendering the page
    end_time = time.time()

    # Calculate total time, including query and rendering
    total_load_time = end_time - start_time
    print(f"Total page load time: {total_load_time} seconds")

    # Pass result and total load time to the template
    return render_template("welcome.html", results=result, total_load_time=total_load_time)



@crm.route("/add_customers", methods=["GET"])
def customers():
    companies = session.query(BDVersicherungsunternehmen).all() 
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
