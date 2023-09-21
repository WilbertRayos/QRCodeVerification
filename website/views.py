from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash
from . import db
from .models import Users, SSLSES, CSSR
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from uuid import uuid4
import qrcode
from os import path


views = Blueprint("views", __name__)

@views.route("/cssr", methods=['GET', 'POST'])
@login_required
def cssr():
    if request.method == "POST":
        certificate_number = request.form.get("certificateNumber")
        ship_name = request.form.get("nameOfShip")
        distinctive_number = request.form.get("distinctiveNumber")
        port_of_registry = request.form.get("portOfRegistry")
        gross_tonnage = request.form.get("grossTonnage")
        sea_areas = request.form.get("seaAreas")
        imo_number = request.form.get("imoNumber")
        valid_until = request.form.get("validUntil")
        

        if not certificate_number:
            flash('Please indicate Certificate Number', category="error")
        elif not ship_name:
            flash('Please indicate Name of Ship', category="error")
        elif not distinctive_number:
            flash('Please indicate Distinctive number/letters', category="error")
        elif not port_of_registry:
            flash('Please indicate Port of Registry', category="error")
        elif not gross_tonnage:
            flash('Please indicate Gross Tonnage', category="error")
        elif not sea_areas:
            flash('Please indicate Sea', category="error")
        elif not imo_number:
            flash('Please indicate Certificate Number', category="error")
        elif not valid_until:
            flash('Please indicate Certificate Number', category="error")
        else:
            qr_text = f"{datetime.now().strftime('%Y%m-%d%H-%M%S-')}{str(uuid4())}"

            new_license = CSSR(certificate_number=certificate_number, 
                            ship_name=ship_name, 
                            distinctive_number=distinctive_number, 
                            port_of_registry=port_of_registry, 
                            gross_tonnage=gross_tonnage, 
                            sea_areas=sea_areas, 
                            imo_number=imo_number, 
                            valid_until=valid_until, 
                            qr_text=qr_text)
            db.session.add(new_license)
            db.session.commit()
            img = qrcode.make(f'https://sscdauthentication.ntc.gov.ph:40000/result/{qr_text}')
            
            try:
                qr_loc = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], f'{qr_text}.png')
                img.save(qr_loc)
                flash('Certificate Saved', category="success")
            except Exception as e:
                print(e)
                print(traceback.print_exc())

        return redirect(url_for("views.cssr"))

    return render_template("cssr.html", user=current_user)

@views.route("/sslses", methods=['GET', 'POST'])
@login_required
def sslses():
    if request.method == "POST":
        # add validation
        application_status = request.form.get("applicationStatus")
        certificate_number = request.form.get("certificateNumber")
        ship_name = request.form.get("nameOfShip")
        call_sign = request.form.get("callSign")
        imo_number = request.form.get("imoNumber")
        aaic = request.form.get("AAIC")
        class_type = request.form.get("cls")
        ship_owner = request.form.get("ownerOfShip")

        if not application_status:
            flash('Please indicate Status', category="error")
        elif not certificate_number:
            flash('Please indicate Certificate Number', category="error")
        elif not ship_name:
            flash('Please indicate Certificate Number', category="error")
        elif not call_sign:
            flash('Please indicate Certificate Number', category="error")
        elif not imo_number:
            flash('Please indicate Certificate Number', category="error")
        elif not aaic:
            flash('Please indicate Certificate Number', category="error")
        elif not class_type:
            flash('Please indicate Certificate Number', category="error")
        elif not ship_owner:
            flash('Please indicate Certificate Number', category="error")
        else:
            qr_text = f"{datetime.now().strftime('%Y%m-%d%H-%M%S-')}{str(uuid4())}"


            new_license = SSLSES(stats=application_status, 
                                certificate_number=certificate_number, 
                                ship_name=ship_name, 
                                call_sign=call_sign, 
                                imo_number=imo_number, 
                                aaic=aaic, 
                                class_type=class_type, 
                                ship_owner=ship_owner, 
                                qr_text=qr_text)
             
            db.session.add(new_license)
            db.session.commit()
            img = qrcode.make(f'https://sscdauthentication.ntc.gov.ph:40000/result/{qr_text}')
            
            qr_loc = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], f'{qr_text}.png')
            img.save(qr_loc)
            flash('Certificate Successfully Added to Database', category="Success")
        
        return redirect(url_for("views.sslses"))
 
    return render_template("sslses.html", user=current_user)

@views.route("/result/<qr_text>")
def result(qr_text):
    if qr_text:
        cssr = CSSR.query.filter_by(qr_text=qr_text).first()
        if cssr:
            return render_template("result.html", user=current_user, cert_categ="cssr", cssr=cssr)
        else:
            sslses = SSLSES.query.filter_by(qr_text=qr_text).first()
            if sslses:
                return render_template("result.html", user=current_user, cert_categ="sslses", sslses=sslses)
   
    return render_template("result.html", user=current_user)

@views.route("/sslses_list", methods=["POST", "GET"])
@login_required
def sslses_list():
    all_sslses = SSLSES.query.order_by(SSLSES.id.desc()).all()
    
    if request.method == "POST":
        entry_id = request.form.get("entryID")
        application_status = request.form.get("applicationStatus")
        certificate_number = request.form.get("certificateNumber")
        ship_name = request.form.get("nameOfShip")
        call_sign = request.form.get("callSign")
        imo_number = request.form.get("imoNumber")
        aaic = request.form.get("AAIC")
        class_type = request.form.get("cls")
        ship_owner = request.form.get("ownerOfShip")

        if not entry_id:
            flash('Invalid ID', category="error")
        elif not application_status:
            flash('Please indicate Status ', category="error")
        elif not certificate_number:
            flash('Please indicate Certificate Number', category="error")
        elif not ship_name:
            flash('Please indicate the Name of Ship', category="error")
        elif not call_sign:
            flash('Please indicate Call Sign', category="error")
        elif not imo_number:
            flash('Please indicate IMO Number', category="error")
        elif not aaic:
            flash('Please indicate AAIC', category="error")
        elif not class_type:
            flash('Please indicate Class', category="error")
        elif not ship_owner:
            flash('Please indicate the Owner of Ship', category="error")
        else:
            entry = SSLSES.query.filter_by(id=entry_id).first()
            if not entry:
                flash('No entry found in the database. Please create new entry', category="error")
            else:
                entry.stats = application_status
                entry.certificate_number = certificate_number
                entry.ship_name = ship_name
                entry.call_sign = call_sign
                entry.imo_number = imo_number
                entry.aaic = aaic
                entry.class_type = class_type
                entry.ship_owner = ship_owner
                db.session.add(entry)
                db.session.commit()
                flash('Entry has been modified successfully', category="success")

        return redirect(url_for("views.sslses_list"))
            
    
    return render_template("sslses_list.html", user=current_user, all_sslses=all_sslses)

@views.route("/cssr_list", methods=["GET", "POST"])
@login_required
def cssr_list():
    all_cssr = CSSR.query.order_by(CSSR.id.desc()).all()
    if request.method == "POST":
        entry_id = request.form.get("entryID")
        certificate_number = request.form.get("certificateNumber")
        ship_name = request.form.get("nameOfShip")
        distinctive_number = request.form.get("distinctiveNumber")
        port_of_registry = request.form.get("portOfRegistry")
        gross_tonnage = request.form.get("grossTonnage")
        sea_areas = request.form.get("seaAreas")
        imo_number = request.form.get("imoNumber")
        valid_until = request.form.get("validUntil")

        if not entry_id:
            flash('Invalid ID', category="error")
        elif not certificate_number:
            flash('Please indicate Certificate Number', category="error")
        elif not ship_name:
            flash('Please indicate the Ship Name', category="error")
        elif not distinctive_number:
            flash('Please indicate Distinctive Number/Letters', category="error")
        elif not port_of_registry:
            flash('Please indicate Port of Registry', category="error")
        elif not gross_tonnage:
            flash('Please indicate Sea Areas in which ship is certified to operate (Reg IV/2)', category="error")
        elif not imo_number:
            flash('Please indicate IMO Number', category="error")
        elif not valid_until:
            flash('Please indicate Valid Until', category="error")
        else:
            entry = CSSR.query.filter_by(id=entry_id).first()
            entry.certificate_number = certificate_number
            entry.ship_name = ship_name
            entry.distinctive_number = distinctive_number
            entry.port_of_registry = port_of_registry
            entry.gross_tonnage = gross_tonnage
            entry.sea_areas = sea_areas
            entry.imo_number = imo_number
            entry.valid_until = valid_until
            db.session.add(entry)
            db.session.commit()
            flash('Entry has been modified successfully', category="success")
        return redirect(url_for("views.cssr_list"))

    return render_template("cssr_list.html", user=current_user, all_cssr=all_cssr)
