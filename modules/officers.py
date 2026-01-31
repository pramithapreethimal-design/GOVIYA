from flask import Blueprint, render_template, request
from extensions import mysql
from flask_login import login_required

officers_bp = Blueprint('officers', __name__)

@officers_bp.route('/officers')
@login_required
def list_officers():
    # Get the selected district from the dropdown (default to 'All')
    district_filter = request.args.get('district', '')
    
    cur = mysql.connection.cursor()
    
    if district_filter:
        # Show officers only for the selected district
        cur.execute("SELECT * FROM agriculture_officers WHERE district = %s", [district_filter])
    else:
        # Show all officers if no filter is selected
        cur.execute("SELECT * FROM agriculture_officers")
        
    officers = cur.fetchall()
    
    # Get a list of unique districts for the dropdown menu
    cur.execute("SELECT DISTINCT district FROM agriculture_officers")
    districts = [row[0] for row in cur.fetchall()]
    
    cur.close()
    
    return render_template('officers/contact_list.html', officers=officers, districts=districts, selected_district=district_filter)