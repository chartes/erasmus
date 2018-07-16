from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint

from . import db, login_manager
from .modeles.donnees import Edition, Exemplaire, Bibliothecae, Provenance, Reference, Bibliographie, Citation, Catalogue
from .constantes import EDITION_PAR_PAGE
from .modeles.utilisateurs import User
from flask_login import login_user, current_user, logout_user, login_required

main_bp = Blueprint(
    'main_bp',
    __name__,
)


@main_bp.route("/")
def accueil():
    """ Route permettant l'affichage de la page d'accueil
        """
    return render_template("pages/accueil.html", nom="Erasmus")


@main_bp.route("/bibliotheques")
def all_libraries():
    """Route permettant l'affichage d'une liste des bibliothèques"""
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    libraries = Bibliothecae.query.order_by(Bibliothecae.bibliothecae_library).paginate(page=page,
                                                                                        per_page=EDITION_PAR_PAGE)
    return render_template("pages/all_libraries.html", nom="Erasmus", libraries=libraries, page=page)


@main_bp.route("/editions")
def all_issues():
    """Route permettant l'affichage d'une liste des éditions"""
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    issues = Edition.query.order_by(Edition.edition_short_title).paginate(page=page, per_page=EDITION_PAR_PAGE)
    return render_template("pages/all_issues.html", nom="Erasmus", issues=issues, page=page)


@main_bp.route("/exemplaires_par_possesseur")
def exemplaires_par_possesseur():
    """Route permettant l'affichage d'une liste des exemplaires par possesseur"""
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    provenances = Provenance.query.order_by(Provenance.provenance_possesseur).paginate(page=page,
                                                                                       per_page=EDITION_PAR_PAGE)

    return render_template("pages/exemplaires_par_possesseur.html", nom="Erasmus", provenances=provenances, page=page)


@main_bp.route("/edition/<int:edition_id>")
def issue(edition_id):
    """Route permettant l'affichage d'une édition
    :param edition_id : identifiant numérique de l'édition récupéré depuis la page notice
    """
    unique_issue = Edition.query.get(edition_id)
    exemplaires = unique_issue.exemplaire
    citations = unique_issue.citation
    references = unique_issue.reference
    digitals = unique_issue.digital

    return render_template("pages/issue.html", nom="Erasmus", issue=unique_issue, exemplaires=exemplaires,
                           citations=citations, references=references, digitals=digitals)


@main_bp.route("/bibliographies")
def all_bibliographies():
    """Route permettant l'affichage d'une liste des oeuvres"""
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    bibliographies = Bibliographie.query.order_by(Bibliographie.bibliographie_code).paginate(page=page,
                                                                                             per_page=EDITION_PAR_PAGE)
    return render_template("pages/all_bibliographies.html", nom="Erasmus", bibliographies=bibliographies, page=page)


@main_bp.route("/bibliographie/<int:bibliographie_id>")
def bibliographie(bibliographie_id):
    """Route permettant l'affichage d'une bibliographie
        :param bibliographie_id : identifiant numérique de l'oeuvre récupéré depuis la page notice
        """
    unique_bibliographie = Bibliographie.query.get(bibliographie_id)
    references = unique_bibliographie.reference

    return render_template("pages/bibliographie.html", nom="Erasmus", bibliographie=unique_bibliographie,
                           references=references)


@main_bp.route("/ajout_bibliographie", methods=["GET", "POST"])
def ajout_bibliographie():
    """ Route gérant les ajouts des oeuvres
        :return: page html d'ajout d'un oeuvre
        """

    if request.method == "POST":
        statut, donnees = Bibliographie.ajout_bibliographie(
            code=request.form.get('code'),
            author=request.form.get('author'),
            bibliReference=request.form.get('bibliReference'),
            title=request.form.get('title'),
            imprint=request.form.get('imprint'),
            urlLink=request.form.get('urlLink'),
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_bibliographie.html")
    else:
        return render_template("pages/ajout_bibliographie.html")


@main_bp.route("/modif_bibliographie/<int:bibliographie_id>", methods=["GET", "POST"])
def modif_bibliographie(bibliographie_id):
    """ Route permettant de modifier un formulaire avec les données d'un oeuvre
       :param bibliographie_id: identifiant numérique de l'oeuvre récupéré depuis la page notice
       """
    unique_bibliographie = Bibliographie.query.get(bibliographie_id)
    if request.method == "POST":
        bibliographie = Bibliographie.query.get(bibliographie_id)
        statut, donnees = Bibliographie.modif_bibliographie(
            id=bibliographie_id,
            code=request.form.get('code'),
            author=request.form.get('author'),
            bibliReference=request.form.get('bibliReference'),
            title=request.form.get('title'),
            imprint=request.form.get('imprint'),
            urlLink=request.form.get('urlLink'),

        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('bibliographie', bibliographie_id=bibliographie.bibliographie_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/modif_bibliographie.html")
    else:
        return render_template("pages/modif_bibliographie.html", bibliographie=unique_bibliographie)

@main_bp.route("/catalogues")
def all_catalogues():
    """Route permettant l'affichage d'une liste des catalogues"""
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    catalogues = Catalogue.query.order_by(Catalogue.catalogue_nom_abrege).paginate(page=page, per_page=EDITION_PAR_PAGE)
    return render_template("pages/all_catalogues.html", nom="Erasmus", catalogues=catalogues, page=page)

@main_bp.route("/catalogue/<int:catalogue_id>")
def catalogue(catalogue_id):
    """Route permettant l'affichage d'un catalogue
            :param catalogue_id : identifiant numérique du catalogue récupéré depuis la page notice
            """
    unique_catalogue = Catalogue.query.get(catalogue_id)


    return render_template("pages/catalogue.html", nom="Erasmus", catalogue=unique_catalogue)

@main_bp.route("/ajout_catalogue", methods=["GET", "POST"])
def ajout_catalogue():
    """ Route gérant les ajouts des catalogues
        :return: page html d'ajout de catalogue
        """

    if request.method == "POST":
        statut, donnees = Catalogue.ajout_catalogue(
            nom=request.form.get('nom'),
            nom_abrege=request.form.get('nom_abrege'),
            site=request.form.get('site')
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_catalogue.html")
    else:
        return render_template("pages/ajout_catalogue.html")

@main_bp.route("/modif_catalogue/<int:catalogue_id>", methods=["GET", "POST"])
def modif_catalogue(catalogue_id):
    """ Route permettant de modifier un formulaire avec les données d'un catalogue
        :param catalogue_id: identifiant numérique du catalogue récupéré depuis la page notice
    """
    unique_catalogue = Catalogue.query.get(catalogue_id)
    if request.method == "POST":
        catalogue = Catalogue.query.get(catalogue_id)
        statut, donnees = Catalogue.modif_catalogue(
            id=catalogue_id,
            nom=request.form.get('nom'),
            nom_abrege=request.form.get('nom_abrege'),
            site=request.form.get('site')

        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('catalogue', catalogue_id=catalogue.catalogue_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/modif_catalogue.html")
    else:
        return render_template("pages/modif_catalogue.html", catalogue=unique_catalogue)


@main_bp.route("/bibliotheque/<int:bibliothecae_id>")
def library(bibliothecae_id):
    """Route permettant l'affichage d'une bibliothèque
    :param bibliothecae_id : identifiant numérique de la bibliothèque récupéré depuis la page notice
    """
    unique_bibliotheque = Bibliothecae.query.get(bibliothecae_id)

    exemplaires = unique_bibliotheque.exemplaire

    return render_template("pages/bibliotheque.html", nom="Erasmus", bibliotheque=unique_bibliotheque,
                           exemplaires=exemplaires)


@main_bp.route("/ajout_bibliotheque", methods=["GET", "POST"])
def ajout_bibliotheque():
    """ Route gérant les ajouts des bibliothèques
        :return: page html d'ajout d'une bibliothèque
        """

    if request.method == "POST":
        statut, donnees = Bibliothecae.ajout_bibliotheque(
            library=request.form.get('library'),
            adresse=request.form.get('adresse'),
            ville=request.form.get('ville'),
            pays=request.form.get('pays'),
            web=request.form.get('web')
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_bibliotheque.html")
    else:
        return render_template("pages/ajout_bibliotheque.html")


@main_bp.route("/modif_bibliotheque/<int:bibliothecae_id>", methods=["GET", "POST"])
def modif_bibliotheque(bibliothecae_id):
    """ Route permettant de modifier un formulaire avec les données d'une bibliothèque
        :param bibliothecae_id: identifiant numérique de la bibliothèque récupéré depuis la page notice
    """
    unique_bibliotheque = Bibliothecae.query.get(bibliothecae_id)
    if request.method == "POST":
        bibliotheque = Bibliothecae.query.get(bibliothecae_id)
        statut, donnees = Bibliothecae.modif_bibliotheque(
            id=bibliothecae_id,
            library=request.form.get('library'),
            adresse=request.form.get('adresse'),
            ville=request.form.get('ville'),
            pays=request.form.get('pays'),
            web=request.form.get('web')
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('library', bibliothecae_id=bibliotheque.bibliothecae_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/modif_bibliotheque.html")
    else:
        return render_template("pages/modif_bibliotheque.html", bibliotheque=unique_bibliotheque)


@main_bp.route("/exemplaire/<int:exemplaire_id>")
def exemplar(exemplaire_id):
    """Route permettant l'affichage d'un exemplaire
        :param exemplaire_id : identifiant numérique de l'exemplaire récupéré depuis la page notice
        """
    unique_exemplar = Exemplaire.query.get(exemplaire_id)
    edition_exemplaire = Edition.query.get(unique_exemplar.exemplaire_edition_id)
    provenances = unique_exemplar.provenance

    return render_template("pages/exemplaires.html", nom="Erasmus", exemplar=unique_exemplar,
                           edition=edition_exemplaire, provenances=provenances)


@main_bp.route("/creer_edition", methods=["GET", "POST"])
def creer_edition():
    """ Route gérant les ajouts des éditions
        :return: page html d'ajout d'une édition
        """
    dates = list(range(1450, 1605, 1))

    if request.method == "POST":
        statut, donnees = Edition.creer_edition(
            short_title=request.form.get("short_title", None),
            title_notes=request.form.get("title_notes"),
            uniform_title=request.form.get("uniform_title"),
            full_title=request.form.get("parallel_title"),
            author_first=request.form.get("author_first", None),
            author_second=request.form.get("author_second"),
            publisher=request.form.get("publisher", None),
            prefaceur=request.form.get("prefaceur"),
            translator=request.form.get("translator", None),
            nomRejete=request.form.get("nomRejete", None),
            dateInferred=request.form.get("dateInferred", None),
            displayDate=request.form.get("displayDate", None),
            cleanDate=request.form.get("cleanDate", None),
            languages=request.form.get("languages", None),
            placeInferred=request.form.get("placeInferred", None),
            place=request.form.get("place", None),
            place2=request.form.get("place2", None),
            placeClean=request.form.get("placeClean", None),
            country=request.form.get("country", None),
            format=request.form.get("format"),
            formatNotes=request.form.get("formatNotes"),
            imprint=request.form.get("imprint", None),
            signatures=request.form.get("signatures"),
            PpFf=request.form.get("PpFf"),
            remarks=request.form.get("remarks"),
            colophon=request.form.get("colophon"),
            illustrated=request.form.get("illustrated"),
            typographicMaterial=request.form.get("typographicMaterial"),
            sheets=request.form.get("sheets"),
            typeNotes=request.form.get("typeNotes"),
            fb=request.form.get("fb"),
            correct=request.form.get("correct"),
            locFingerprints=request.form.get("locFingerprints"),
            stcnFingerprints=request.form.get("stcnFingerprints"),
            tpt=request.form.get("tpt"),
            notes=request.form.get("notes"),
            printer=request.form.get("printer"),
            urlImage=request.form.get("urlImage"),
            class0=request.form.get("class0", None),
            class1=request.form.get("class1", None),
            class2=request.form.get("class2", None),
            digital=request.form.get("digital", None),
            fulltext=request.form.get("fulltext", None),
            tpimage=request.form.get("tpimage", None),
            privelege=request.form.get("privelege", None),
            dedication=request.form.get("dedication", None),
            reference=request.form.get("reference", None),
            citation=request.form.get("citation", None),
            user_id=current_user.get_id()

        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/creer_edition.html", dates=dates)
    else:
        return render_template("pages/creer_edition.html", dates=dates)


@main_bp.route("/modif_edition/<int:edition_id>", methods=["GET", "POST"])
def modif_edition(edition_id):
    """ Route permettant de modifier un formulaire avec les données d'une édition
        :param edition_id: identifiant numérique de l'édition récupéré depuis la page notice
    """
    unique_edition = Edition.query.get(edition_id)

    if request.method == "POST":
        edition = Edition.query.get(edition_id)
        status, donnees = Edition.modif_edition(
            id=edition_id,
            short_title=request.form.get("short_title"),
            title_notes=request.form.get("title_notes"),
            uniform_title=request.form.get("uniform_title"),
            full_title=request.form.get("parallel_title"),
            author_first=request.form.get("author_first"),
            author_second=request.form.get("author_second"),
            publisher=request.form.get("publisher"),
            prefaceur=request.form.get("prefaceur"),
            translator=request.form.get("translator"),
            nomRejete=request.form.get("nomRejete"),
            dateInferred=request.form.get("dateInferred"),
            displayDate=request.form.get("displayDate"),
            cleanDate=request.form.get("cleanDate"),
            languages=request.form.get("languages"),
            placeInferred=request.form.get("placeInferred"),
            place=request.form.get("place"),
            place2=request.form.get("place2"),
            placeClean=request.form.get("placeClean"),
            country=request.form.get("country"),
            format=request.form.get("format"),
            formatNotes=request.form.get("formatNotes"),
            imprint=request.form.get("imprint"),
            signatures=request.form.get("signatures", None),
            PpFf=request.form.get("PpFf", None),
            remarks=request.form.get("remarks", None),
            colophon=request.form.get("colophon", None),
            illustrated=request.form.get("illustrated", None),
            typographicMaterial=request.form.get("typographicMaterial", None),
            sheets=request.form.get("sheets", None),
            typeNotes=request.form.get("typeNotes", None),
            fb=request.form.get("fb", None),
            correct=request.form.get("correct", None),
            locFingerprints=request.form.get("locFingerprints", None),
            stcnFingerprints=request.form.get("stcnFingerprints", None),
            tpt=request.form.get("tpt", None),
            notes=request.form.get("notes", None),
            printer=request.form.get("printer", None),
            urlImage=request.form.get("urlImage", None),
            class0=request.form.get("class0", None),
            class1=request.form.get("class1", None),
            class2=request.form.get("class2", None),
            digital=request.form.get("digital", None),
            fulltext=request.form.get("fulltext", None),
            tpimage=request.form.get("tpimage", None),
            privelege=request.form.get("privelege", None),
            dedication=request.form.get("dedication", None),
            reference=request.form.get("reference", None),
            citation=request.form.get("citation", None),
            user_id=current_user.get_id()
        )

        if status is True:
            flash('Merci de votre contribution', 'success')
            return redirect(url_for('issue', edition_id=edition.edition_id))

        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")

            return render_template("pages/modif_commentaire.html")
    return render_template("pages/modif_edition.html", nom="Erasmus", edition=unique_edition)


@main_bp.route("/ajout_exemplaire/<int:identifier>", methods=["GET", "POST"])
def ajout_exemplaire(identifier):
    """ Route gérant les ajouts des exemplaires
    :param identifier : identifiant d'édition
    :return: page html d'ajout d'un exemplaire
    """

    if request.method == "GET":
        bibliotheques = Bibliothecae.query.all()
        edition = Edition.query.get(identifier)

        return render_template("pages/ajout_exemplaire.html", bibliotheques=bibliotheques, edition=edition)

    if request.method == "POST":
        edition = Edition.query.get(identifier)
        statut, donnees = Exemplaire.ajout_exemplaire(
            pressmark=request.form.get('pressmark'),
            hauteur=request.form.get('hauteur'),
            variantesEdition=request.form.get('variantesEdition'),
            digitalURL=request.form.get('digitalURL'),
            etatMateriel=request.form.get('etatMateriel'),
            notes=request.form.get('notes'),
            provenances=request.form.get('provenances'),
            locFingerprint=request.form.get('locFingerprint'),
            stcnFingerprint=request.form.get('stcnFingerprint'),
            annotationManuscrite=request.form.get('annotationManuscrite'),
            largeur=request.form.get('largeur'),
            recueilFactice=request.form.get('recueilFactice'),
            reliure=request.form.get('reliure'),
            reliureXVI=request.form.get('reliureXVI'),
            relieAvec=request.form.get('relieAvec'),
            edition_id=identifier,
            bibliothecae_id=request.form.get('library'),
            user_id=current_user.get_id()
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('issue', edition_id=edition.edition_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_exemplaire.html")
    else:
        return render_template("pages/ajout_exemplaire.html")


@main_bp.route("/modif_exemplaire/<int:exemplaire_id>", methods=["GET", "POST"])
def modif_exemplaire(exemplaire_id):
    """ Route permettant de modifier un exemplaire avec les données d'un catalogue
        :param exemplaire_id: identifiant numérique de l'exemplaire récupéré depuis la page notice
    """
    unique_exemplaire = Exemplaire.query.get(exemplaire_id)
    bibliotheques = Bibliothecae.query.order_by(Bibliothecae.bibliothecae_library).all()
    if request.method == "POST":
        bibliotheques = Bibliothecae.query.all()
        exemplaire = Exemplaire.query.get(exemplaire_id)
        statut, donnees = Exemplaire.modif_exemplaire(
            id=exemplaire_id,
            pressmark=request.form.get('pressmark'),
            hauteur=request.form.get('hauteur'),
            variantesEdition=request.form.get('variantesEdition'),
            digitalURL=request.form.get('digitalURL'),
            etatMateriel=request.form.get('etatMateriel'),
            notes=request.form.get('notes'),
            provenances=request.form.get('provenances'),
            locFingerprint=request.form.get('locFingerprint'),
            stcnFingerprint=request.form.get('stcnFingerprint'),
            annotationManuscrite=request.form.get('annotationManuscrite'),
            largeur=request.form.get('largeur'),
            recueilFactice=request.form.get('recueilFactice'),
            reliure=request.form.get('reliure'),
            reliureXVI=request.form.get('reliureXVI'),
            relieAvec=request.form.get('relieAvec'),
            bibliothecae_id=request.form.get('library'),
            user_id=current_user.get_id(),
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('exemplar', exemplaire_id=exemplaire.exemplaire_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/modif_exemplaire.html", bibliotheques=bibliotheques)
    else:
        return render_template("pages/modif_exemplaire.html", exemplaire=unique_exemplaire, bibliotheques=bibliotheques)


@main_bp.route("/ajout_provenance/<int:exemplaire_id>", methods=["GET", "POST"])
def ajout_provenance(exemplaire_id):
    """ Route gérant les ajouts des provenances
    :param exemplaire_id : identifiant d'exemplaire
    :return: page html d'ajout d'une provenance
    """

    if request.method == "GET":
        exemplaire = Exemplaire.query.get(exemplaire_id)

        return render_template("pages/ajout_provenance.html", exemplaire=exemplaire)

    if request.method == "POST":
        exemplaire = Exemplaire.query.get(exemplaire_id)
        statut, donnees = Provenance.ajout_provenance(

            exlibris=request.form.get('exlibris'),
            exdono=request.form.get('exdono'),
            envoi=request.form.get('envoi'),
            notesManuscrites=request.form.get('notesManuscrites'),
            armesPeintes=request.form.get('armesPeintes'),
            restitue=request.form.get('restitue'),
            mentionEntree=request.form.get('mentionEntree'),
            estampillesCachets=request.form.get('estampillesCachets'),
            possesseur=request.form.get('possesseur'),
            possesseur_formeRejetee=request.form.get('possesseur_formeRejetee'),
            reliure_provenance=request.form.get('reliure_provenance'),
            notes=request.form.get('notes'),
            exemplaire_id=exemplaire_id
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('exemplar', exemplaire_id=exemplaire.exemplaire_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_provenance.html", exemplaire=exemplaire)
    else:
        return render_template("pages/ajout_provenance.html")


@main_bp.route("/modif_provenance/<int:provenance_id>", methods=["GET", "POST"])
def modif_provenance(provenance_id):
    """ Route permettant de modifier un formulaire avec les données d'une provenance
            :param provenance_id: identifiant numérique de la catalogue récupéré depuis la page notice
        """
    unique_provenance = Provenance.query.get(provenance_id)

    if request.method == "POST":
        unique_provenance = Provenance.query.get(provenance_id)
        statut, donnees = Provenance.modif_provenance(

            id=provenance_id,
            exlibris=request.form.get('exlibris'),
            exdono=request.form.get('exdono'),
            envoi=request.form.get('envoi'),
            notesManuscrites=request.form.get('notesManuscrites'),
            armesPeintes=request.form.get('armesPeintes'),
            restitue=request.form.get('restitue'),
            mentionEntree=request.form.get('mentionEntree'),
            estampillesCachets=request.form.get('estampillesCachets'),
            possesseur=request.form.get('possesseur'),
            reliure_provenance=request.form.get('reliure_provenance'),
            possesseur_formeRejetee=request.form.get('possesseur_formeRejetee'),
            notes=request.form.get('notes'),
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('exemplar', exemplaire_id=unique_provenance.provenance_exemplaire_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/modif_provenance.html")
    else:
        return render_template("pages/modif_provenance.html", provenance=unique_provenance)


@main_bp.route("/ajout_reference/<int:edition_id>", methods=["GET", "POST"])
def ajout_reference(edition_id):
    """ Route gérant les ajouts des référence
        :param edition_id : identifiant d'édition
        :return: page html d'ajout d'une référence
        """

    if request.method == "GET":
        bibliographies = Bibliographie.query.all()
        edition = Edition.query.get(edition_id)

        return render_template("pages/ajout_reference.html", edition=edition, bibliographies=bibliographies)

    if request.method == "POST":
        edition = Edition.query.get(edition_id)
        statut, donnees = Reference.ajout_reference(

            volume=request.form.get('volume'),
            page=request.form.get('page'),
            recordNumber=request.form.get('recordNumber'),
            note=request.form.get('note'),
            bibliographie_id=request.form.get('oeuvre'),
            edition_id=edition_id
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('issue', edition_id=edition.edition_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_reference.html")
    else:
        return render_template("pages/ajout_reference.html")


@main_bp.route("/modif_reference/<int:reference_id>", methods=["GET", "POST"])
def modif_reference(reference_id):
    """ Route permettant de modifier un formulaire avec les données d'une référence
            :param reference_id: identifiant numérique de la référence récupéré depuis la page notice
        """
    bibliographies = Bibliographie.query.all()
    unique_reference = Reference.query.get(reference_id)

    if request.method == "POST":

        statut, donnees = Reference.modif_reference(

            id=reference_id,
            volume=request.form.get('volume'),
            page=request.form.get('page'),
            recordNumber=request.form.get('recordNumber'),
            note=request.form.get('note'),
            bibliographie_id=request.form.get('oeuvre')

        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('issue', edition_id=unique_reference.reference_edition_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/modif_reference.html", bibliographies=bibliographies)
    else:
        return render_template("pages/modif_reference.html", reference=unique_reference, bibliographies=bibliographies)


@main_bp.route("/ajout_citation/<int:edition_id>", methods=["GET", "POST"])
def ajout_citation(edition_id):
    """ Route gérant les ajouts des citations
        :param edition_id : identifiant d'édition
        :return: page html d'ajout d'une citation
        """

    if request.method == "GET":
        edition = Edition.query.get(edition_id)
        catalogues = Catalogue.query.all()

        return render_template("pages/ajout_citation.html", edition=edition, catalogues=catalogues)

    if request.method == "POST":
        edition = Edition.query.get(edition_id)
        statut, donnees = Citation.ajout_citation(

            dbnumber=request.form.get('dbnumber'),
            url=request.form.get('url'),
            edition_id=edition_id,
            catalogue_id=request.form.get('dbname')
        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('issue', edition_id=edition.edition_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/ajout_citation.html")
    else:
        return render_template("pages/ajout_citation.html")


@main_bp.route("/modif_citation/<int:citation_id>", methods=["GET", "POST"])
def modif_citation(citation_id):
    """ Route permettant de modifier un formulaire avec les données d'une citation
            :param catalogue_id: identifiant numérique de la citation récupéré depuis la page notice
        """
    unique_citation = Citation.query.get(citation_id)
    catalogues = Catalogue.query.all()

    if request.method == "POST":

        statut, donnees = Citation.modif_citation(

            id=citation_id,
            dbnumber=request.form.get('dbnumber'),
            url=request.form.get('url'),
            catalogue_id=request.form.get('dbname')

        )
        if statut is True:
            flash("Enregistrement effectué", "success")
            return redirect(url_for('issue', edition_id=unique_citation.citation_edition_id))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/modif_citation.html")
    else:
        return render_template("pages/modif_citation.html", citation=unique_citation , catalogues=catalogues)


@main_bp.route("/recherche")
def recherche():
    """ Route permettant la recherche plein-texte par plusieurs champs
    """

    resultats = []


    titre = "Recherche"
    resultats = Edition.recherche_avancee(request.args).order_by(Edition.edition_short_title)

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre

    )


@main_bp.route("/recherche_avancee")
def recherche_avancee():
    return render_template("pages/rech_av_form.html", nom="Erasmus")


@main_bp.route("/recherche_rapide")
def recherche_rapide():
    """ Route permettant la recherche plein-texte à partir de la navbar
    """
    motcle = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    # Création d'une liste vide de résultat (par défaut, vide si pas de mot-clé)
    resultats = []

    # cherche les mots-clés dans les champs : author_first, author_second, place, short_title,
    #languages, prefaceur, printer, nomRejete, place2, class0, class1, class2, displayDate,
    #cleanDate, country, full_title, publisher, translator, imprint

    titre = "Recherche"
    if motcle:
        resultats = Edition.query.filter(db.or_(Edition.edition_author_first.like("%{}%".format(motcle)),
                                                Edition.edition_place.like("%{}%".format(motcle)),
                                                Edition.edition_author_second.like("%{}%".format(motcle)),
                                                Edition.edition_languages.like("%{}%".format(motcle)),
                                                Edition.edition_prefaceur.like("%{}%".format(motcle)),
                                                Edition.edition_printer.like("%{}%".format(motcle)),
                                                Edition.edition_nomRejete.like("%{}%".format(motcle)),
                                                Edition.edition_place2.like("%{}%".format(motcle)),
                                                Edition.edition_class0.like("%{}%".format(motcle)),
                                                Edition.edition_class1.like("%{}%".format(motcle)),
                                                Edition.edition_class2.like("%{}%".format(motcle)),
                                                Edition.edition_displayDate.like("%{}%".format(motcle)),
                                                Edition.edition_cleanDate.like("%{}%".format(motcle)),
                                                Edition.edition_country.like("%{}%".format(motcle)),
                                                Edition.edition_full_title.like("%{}%".format(motcle)),
                                                Edition.edition_publisher.like("%{}%".format(motcle)),
                                                Edition.edition_translator.like("%{}%".format(motcle)),
                                                Edition.edition_imprint.like("%{}%".format(motcle)),
                                                Edition.edition_short_title.like("%{}%".format(motcle)))
                                         ).order_by(Edition.edition_short_title).paginate(page=page,
                                                                                          per_page=EDITION_PAR_PAGE)
        # si un résultat, renvoie sur la page résultat
        titre = "Résultat de la recherche : `" + motcle + "`"
        return render_template("pages/resultats.html", resultats=resultats, titre=titre, keyword=motcle)


@main_bp.route("/suppression_edition/<int:edition_id>", methods=["GET", "POST"])
def suppression_edition(edition_id):
    """ Route pour gérer la suppresion d'une édition dans la base
        :param edition_id : identifiant numérique de l'édition
        """

    unique_edition = Edition.query.get(edition_id)

    if request.method == "GET":
        return render_template("pages/suppr_edition.html", unique=unique_edition)
    else:
        status = Edition.delete_edition(edition_id=edition_id)
        if status is True:
            flash("Une édition a été supprimée !", "success")
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for('issue', edition_id=unique_edition.edition_id))


@main_bp.route("/suppression_bibliographie/<int:bibliographie_id>", methods=["GET", "POST"])
def suppression_bibliographie(bibliographie_id):
    """ Route pour gérer la suppresion d'un oeuvre dans la base
        :param bibliographie_id : identifiant numérique de l'oeuvre
        """
    unique_bibliographie = Bibliographie.query.get(bibliographie_id)
    if request.method == "GET":
        return render_template("pages/suppression_bibliographie.html", bibliographie=unique_bibliographie)
    else:
        status = Bibliographie.delete_bibliographie(bibliographie_id=bibliographie_id)
        if status is True:
            flash("Une oeuvre a été supprimée !", "success")
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for("main_bp.accueil"))


@main_bp.route("/suppression_citation/<int:citation_id>", methods=["GET", "POST"])
def suppression_citation(citation_id):
    """ Route pour gérer la suppresion d'une citation dans la base
    :param citation_id : identifiant numérique de la citation
    """

    unique_citation = Citation.query.get(citation_id)

    if request.method == "GET":
        return render_template("pages/suppression_citation.html", citation=unique_citation)
    else:
        status = Citation.delete_citation(citation_id=citation_id)
        if status is True:
            flash("La citation a été supprimée !", "success")
            return redirect(url_for('issue', edition_id=unique_citation.citation_edition_id))
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for('issue', edition_id=unique_citation.citation_edition_id))


@main_bp.route("/suppression_bibliotheque/<int:bibliothecae_id>", methods=["GET", "POST"])
def suppression_bibliotheque(bibliothecae_id):
    """ Route pour gérer la suppresion d'une bibliothèque dans la base
        :param bibliothecae_id : identifiant numérique de la bibliothèque
        """
    unique_bibliotheque = Bibliothecae.query.get(bibliothecae_id)
    if request.method == "GET":
        return render_template("pages/suppression_bibliotheque.html", bibliotheque=unique_bibliotheque)
    else:
        status = Bibliothecae.delete_bibliotheque(bibliothecae_id=bibliothecae_id)
        if status is True:
            flash("Une oeuvre a été supprimée !", "success")
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for('library', bibliothecae_id=unique_bibliotheque.bibliothecae_id))


@main_bp.route("/suppression_exemplaire/<int:exemplaire_id>", methods=["GET", "POST"])
def suppression_exemplaire(exemplaire_id):
    """ Route pour gérer la suppresion d'un exemplaire dans la base
        :param exemplaire_id : identifiant numérique de l'exemplaire
        """
    unique_exemplaire = Exemplaire.query.get(exemplaire_id)
    if request.method == "GET":
        return render_template("pages/suppression_exemplaire.html", exemplaire=unique_exemplaire)
    else:
        status = Exemplaire.delete_exemplaire(exemplaire_id=exemplaire_id)
        if status is True:
            flash("Un exemplaire a été supprimé !", "success")
            return redirect(url_for('issue', edition_id=unique_exemplaire.exemplaire_edition_id))
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for('exemplar', exemplaire_id=unique_exemplaire.exemplaire_id))


@main_bp.route("/suppression_provenance/<int:provenance_id>", methods=["GET", "POST"])
def suppression_provenance(provenance_id):
    """ Route pour gérer la suppresion d'une provenance dans la base
        :param provenance_id : identifiant numérique de la provenance
        """
    unique_provenance = Provenance.query.get(provenance_id)
    if request.method == "GET":
        return render_template("pages/suppression_provenance.html", provenance=unique_provenance)
    else:
        status = Provenance.delete_provenance(provenance_id=provenance_id)
        if status is True:
            flash("Une provenance a été supprimée !", "success")
            return redirect(url_for('exemplar', exemplaire_id=unique_provenance.provenance_exemplaire_id))
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for('exemplar', exemplaire_id=unique_provenance.provenance_exemplaire_id))


@main_bp.route("/suppression_reference/<int:reference_id>", methods=["GET", "POST"])
def suppression_reference(reference_id):
    """ Route pour gérer la suppresion d'une référence dans la base
        :param nr_person : identifiant numérique de la référence
        """
    unique_reference = Reference.query.get(reference_id)
    if request.method == "GET":
        return render_template("pages/suppression_reference.html", reference=unique_reference)
    else:
        status = Reference.delete_reference(reference_id=reference_id)
        if status is True:
            flash("Une référence a été supprimée !", "success")
            return redirect(url_for('issue', edition_id=unique_reference.reference_edition_id))
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for('issue', edition_id=unique_reference.reference_edition_id))

@main_bp.route("/suppression_catalogue/<int:catalogue_id>", methods=["GET", "POST"])
def suppression_catalogue(catalogue_id):
    """ Route pour gérer la suppresion d'un catalogue dans la base
        :param nr_person : identifiant numérique du catalogue
        """

    unique_catalogue=Catalogue.query.get(catalogue_id)
    if request.method == "GET":
        return render_template("pages/suppression_catalogue.html", catalogue=unique_catalogue)
    else:
        status = Catalogue.delete_catalogue(catalogue_id=catalogue_id)
        if status is True:
            flash("Un catalogue a été supprimé !", "success")
            return redirect("/")
        else:
            flash("La suppression a échoué.", "danger")
            return redirect(url_for('catalogue', catalogue_id=unique_catalogue.catalogue_id))



@main_bp.route("/register", methods=["GET", "POST"])
@login_required
def inscription():
    """ Route gérant les inscriptions
    :return: page html d'inscription
    """

    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect(url_for('main_bp.accueil'))
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")


@main_bp.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    :return: page html de connection
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect(url_for("main_bp.accueil"))
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("main_bp.accueil"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")

    return render_template("pages/connexion.html")


@main_bp.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """ Route gérant les déconnexions
        :return: page html d'acceuil
        """
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")


    return redirect(url_for("main_bp.accueil"))
