from .. import db



# On crée notre modèle
class Edition(db.Model):
    edition_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    edition_short_title = db.Column(db.Text)
    edition_title_notes = db.Column(db.Text)
    edition_full_title = db.Column(db.Text)
    edition_uniform_title = db.Column(db.Text)
    edition_author_first = db.Column(db.Text, nullable=False)
    edition_author_second = db.Column(db.Text)
    edition_publisher = db.Column(db.Text)
    edition_prefaceur = db.Column(db.Text)
    edition_nomRejete = db.Column(db.Text)
    edition_translator = db.Column(db.Text)
    edition_dateInferred = db.Column(db.Text)
    edition_displayDate = db.Column(db.Text)
    edition_cleanDate = db.Column(db.Text)
    edition_languages = db.Column(db.Text)
    edition_placeInferred = db.Column(db.Text)
    edition_place = db.Column(db.Text)
    edition_place2 = db.Column(db.Text)
    edition_placeClean = db.Column(db.Text)
    edition_country = db.Column(db.Text)
    edition_collator_format = db.Column(db.Text)
    edition_collator_formatNotes = db.Column(db.Text)
    edition_imprint = db.Column(db.Text)
    edition_collator_signatures = db.Column(db.Text)
    edition_collator_PpFf = db.Column(db.Text)
    edition_collator_remarks = db.Column(db.Text)
    edition_collator_colophon = db.Column(db.Text)
    edition_collator_illustrated = db.Column(db.Text)
    edition_collator_typographicMaterial  = db.Column(db.Text)
    edition_collator_sheets = db.Column(db.Text)
    edition_collator_typeNotes = db.Column(db.Text)
    edition_collator_fb = db.Column(db.Text)
    edition_collator_correct  = db.Column(db.Text)
    edition_collator_locFingerprints = db.Column(db.Text)
    edition_collator_stcnFingerprints = db.Column(db.Text)
    edition_collator_tpt = db.Column(db.Text)
    edition_notes = db.Column(db.Text)
    edition_printer = db.Column(db.Text)
    edition_urlImage = db.Column(db.Text)
    edition_class0 = db.Column(db.Text)
    edition_class1 = db.Column(db.Text)
    edition_class2 = db.Column(db.Text)
    edition_digital = db.Column(db.Text)
    edition_fulltext = db.Column(db.Text)
    edition_tpimage = db.Column(db.Text)
    edition_privelege = db.Column(db.Text)
    edition_dedication = db.Column(db.Text)
    edition_reference = db.Column(db.Text)
    edition_citation = db.Column(db.Integer)
    edition_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    exemplaire = db.relationship("Exemplaire", back_populates="edition")
    reference = db.relationship("Reference", back_populates="edition")
    citation = db.relationship("Citation", back_populates="edition")
    digital = db.relationship("Digital", back_populates="edition")
    user = db.relationship("User", back_populates="edition")


    def creer_edition(short_title, title_notes, uniform_title, full_title, author_first, author_second, publisher, prefaceur, nomRejete, translator, dateInferred, displayDate, cleanDate, languages, placeInferred, place, placeClean, place2, country, format, formatNotes, imprint, signatures, PpFf, remarks, colophon, illustrated, typographicMaterial, sheets, typeNotes, fb, correct, locFingerprints, stcnFingerprints, tpt, notes, printer, urlImage, class0, class1, class2, digital, fulltext, tpimage, privelege, dedication, reference, citation, user_id):
        # on vérifie qu'au moins un des trois champs (nom d'auteur, titre et clenDate) est rempli ainsi que celui de la description qui est obligatoire
        erreurs = []
        if not short_title:
            erreurs.append("Le titre fourni est vide")
        if not author_first:
            erreurs.append("Le nom d'auteur fourni est vide")
        if not cleanDate:
            erreurs.append("La date fournie est vide")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs
        """ 
        :param short_title: titre court de l'édition
        :param title_notes : les notes sur le titre
        :param uniform_title : titre uniforme
        :param full_title : titre entier
        :param author_first : premier auteur
        :param author_second : auteur sécondaire
        :param publisher : éditeur
        :param prefaceur : préfacier
        :param nomRejete : formes rejétées des nom d'auteurs
        :param translator : traducteur
        :param dateInferred : date déduite
        :param displayDate : date affichée
        :param cleanDate : date propre
        :param languages : langues d'édition
        :param placeInferred : lieu déduit
        :param place : lieu d'édition
        :param placeClean : lieu propre
        :param place2 : formes rejétés de lieu
        :param country : pays
        :param format : format d'édition
        :param formatNotes : notes sur le format
        :param imprint : imprint
        :param signatures : signatures
        :param PpFf : pages et feuillets
        :param remarks : remarque
        :param colophon : colophon
        :param illustrated : illustrration d'édition
        :param typographicMaterial : matériaux typographiques
        :param sheets : feuilles
        :param typeNotes : notes sur typographie
        :param fb : numéro dans French Vernacular Books
        :param correct : collation correcte
        :param locFingerprints : empreinte LOC
        :param stcnFingerprints : empreinte STCN
        :param tpt : transcription de la page de titre
        :param notes : notes sur édition
        :param printer : imprimeur
        :param urlImage : lien vers image (page de titre)
        :param class0, class1, class2 : classification
        :param digital : disponibilité de version numérique
        :param fulltext : disponibilité de texte entier
        :param tpimage : reproduction page de titre
        :param privelege : notes sur privilège
        :param dedication : notes sur dédicace
        :param reference : notes sur références
        :param citation: notes sur citation
        :param user_id : identifiant de créateur de notice
        :type user_id : int
        :type short_title, title_notes, uniform_title, full_title, author_first, author_second, publisher, prefaceur, nomRejete, translator, dateInferred, displayDate, cleanDate, languages, placeInferred, place, placeClean, place2, country, format, formatNotes, imprint, signatures, PpFf, remarks, colophon, illustrated, typographicMaterial, sheets, typeNotes, fb, correct, locFingerprints, stcnFingerprints, tpt, notes, printer, urlImage, class0, class1, class2, digital, fulltext, tpimage, privelege, dedication, reference, citation: str

        :returns : Booléen
        S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
        Sinon, elle renvoie True, suivi de l'objet mis à jour (ici personne).
        """
        # On rajoute une nouvelle édition
        edition = Edition(
            edition_short_title=short_title,
            edition_title_notes=title_notes,
            edition_uniform_title=uniform_title,
            edition_full_title=full_title,
            edition_author_first=author_first,
            edition_author_second=author_second,
            edition_publisher=publisher,
            edition_prefaceur=prefaceur,
            edition_nomRejete=nomRejete,
            edition_translator=translator,
            edition_dateInferred=dateInferred,
            edition_displayDate=displayDate,
            edition_cleanDate=cleanDate,
            edition_languages=languages,
            edition_placeInferred=placeInferred,
            edition_place=place,
            edition_place2=place2,
            edition_placeClean=placeClean,
            edition_country=country,
            edition_collator_format=format,
            edition_collator_formatNotes=formatNotes,
            edition_imprint=imprint,
            edition_collator_signatures=signatures,
            edition_collator_PpFf=PpFf,
            edition_collator_remarks=remarks,
            edition_collator_colophon=colophon,
            edition_collator_illustrated=illustrated,
            edition_collator_typographicMaterial=typographicMaterial,
            edition_collator_sheets=sheets,
            edition_collator_typeNotes=typeNotes,
            edition_collator_fb=fb,
            edition_collator_correct=correct,
            edition_collator_locFingerprints=locFingerprints,
            edition_collator_stcnFingerprints=stcnFingerprints,
            edition_collator_tpt=tpt,
            edition_notes=notes,
            edition_printer=printer,
            edition_urlImage=urlImage,
            edition_class0=class0,
            edition_class1=class1,
            edition_class2=class2,
            edition_digital=digital,
            edition_fulltext=fulltext,
            edition_tpimage=tpimage,
            edition_privelege=privelege,
            edition_dedication=dedication,
            edition_reference=reference,
            edition_citation=citation,
            edition_user_id=user_id
            
        )
        print(edition)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(edition)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'édition
            return True, edition
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_edition(id, short_title, title_notes, uniform_title, full_title, author_first, author_second, publisher, prefaceur, nomRejete, translator, dateInferred, displayDate, cleanDate, languages, placeInferred, place, placeClean, place2, country, format, formatNotes, imprint, signatures, PpFf, remarks, colophon, illustrated, typographicMaterial, sheets, typeNotes, fb, correct, locFingerprints, stcnFingerprints, tpt, notes, printer, urlImage, class0, class1, class2, digital, fulltext, tpimage, privelege, dedication, reference, citation, user_id):
        """ Modifie les informations de la notice d'une édition
                :param id: l'identifiant de l'édition
                :type id: int
                :param short_title : titre court de l'édition
                :param title_notes : les notes sur le titre
                :param uniform_title : titre uniforme
                :param full_title : titre entier
                :param author_first : premier auteur
                :param author_second : auteur sécondaire
                :param publisher : éditeur
                :param prefaceur : préfacier
                :param nomRejete : formes rejétées des nom d'auteurs
                :param translator : traducteur
                :param dateInferred : date déduite
                :param displayDate : date affichée
                :param cleanDate : date propre
                :param languages : langues d'édition
                :param placeInferred : lieu déduit
                :param place : lieu d'édition
                :param placeClean : lieu propre
                :param place2 : formes rejétés de lieu
                :param country : pays
                :param format : format d'édition
                :param formatNotes : notes sur le format
                :param imprint : imprint
                :param signatures : signatures
                :param PpFf : pages et feuillets
                :param remarks : remarque
                :param colophon : colophon
                :param illustrated : illustrration d'édition
                :param typographicMaterial : matériaux typographiques
                :param sheets : feuilles
                :param typeNotes : notes sur typographie
                :param fb : numéro dans French Vernacular Books
                :param correct : collation correcte
                :param locFingerprints : empreinte LOC
                :param stcnFingerprints : empreinte STCN
                :param tpt : transcription de la page de titre
                :param notes : notes sur édition
                :param printer : imprimeur
                :param urlImage : lien vers image (page de titre)
                :param class0, class1, class2 : classification
                :param digital : disponibilité de version numérique
                :param fulltext : disponibilité de texte entier
                :param tpimage : reproduction page de titre
                :param privelege : notes sur privilège
                :param dedication : notes sur dédicace
                :param reference : notes sur références
                :param citation: notes sur citation
                :param user_id : identifiant de créateur de notice
                :type user_id : int
                :type short_title, title_notes, uniform_title, full_title, author_first, author_second, publisher, prefaceur, nomRejete, translator, dateInferred, displayDate, cleanDate, languages, placeInferred, place, placeClean, place2, country, format, formatNotes, imprint, signatures, PpFf, remarks, colophon, illustrated, typographicMaterial, sheets, typeNotes, fb, correct, locFingerprints, stcnFingerprints, tpt, notes, printer, urlImage, class0, class1, class2, digital, fulltext, tpimage, privelege, dedication, reference, citation: str

                :returns : Booléen
                S'il y a une erreur, la fonction renvoie False suivi d'une liste d'erreurs.
                Sinon, elle renvoie True, suivi de l'objet mis à jour (ici personne).
               """

        edition = Edition.query.get(id)

        edition.edition_short_title = short_title,
        edition.edition_title_notes = title_notes,
        edition.edition_uniform_title = uniform_title,
        edition.edition_full_title = full_title,
        edition.edition_author_first = author_first,
        edition.edition_author_second = author_second,
        edition.edition_publisher = publisher,
        edition.edition_prefaceur = prefaceur,
        edition.edition_nomRejete = nomRejete,
        edition.edition_translator = translator,
        edition.edition_dateInferred = dateInferred,
        edition.edition_displayDate = displayDate,
        edition.edition_cleanDate = cleanDate,
        edition.edition_languages = languages,
        edition.edition_placeInferred = placeInferred,
        edition.edition_place = place,
        edition.edition_place2 = place2,
        edition.edition_placeClean = placeClean,
        edition.edition_country = country,
        edition.edition_collator_format = format,
        edition.edition_collator_formatNotes = formatNotes,
        edition.edition_imprint = imprint,
        edition.edition_collator_signatures = signatures,
        edition.edition_collator_PpFf = PpFf,
        edition.edition_collator_remarks = remarks,
        edition.edition_collator_colophon = colophon,
        edition.edition_collator_illustrated = illustrated,
        edition.edition_collator_typographicMaterial = typographicMaterial,
        edition.edition_collator_sheets = sheets,
        edition.edition_collator_typeNotes = typeNotes,
        edition.edition_collator_fb = fb,
        edition.edition_collator_correct = correct,
        edition.edition_collator_locFingerprints = locFingerprints,
        edition.edition_collator_stcnFingerprints = stcnFingerprints,
        edition.edition_collator_tpt = tpt,
        edition.edition_notes = notes,
        edition.edition_printer = printer,
        edition.edition_urlImage = urlImage,
        edition.edition_class0 = class0,
        edition.edition_class1 = class1,
        edition.edition_class2 = class2,
        edition.edition_digital = digital,
        edition.edition_fulltext = fulltext,
        edition.edition_tpimage = tpimage,
        edition.edition_privelege = privelege,
        edition.edition_dedication = dedication,
        edition.edition_reference = reference,
        edition.edition_citation = citation,
        edition.edition_user_id = user_id

        try:

            db.session.add(edition)
            db.session.commit()

            return True, edition
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def recherche_avancee(champs):
        """
        On effectue la recherche par plusieurs champs (titre, auteur, date, place, pays, printer, possesseur)
        :param champs: Dictionaire de champs avec leurs valerurs
        :type champs: str
        """
        champs = {
            clef: valeur
            for clef, valeur in champs.items()
            if valeur and len(valeur) > 0
        }

        joined = set()
        filtres = []

        if "title" in champs:
            filtres.append(Edition.edition_short_title.like("%{}%".format(champs["title"])))
        if "auteur" in champs:
            filtres.append(Edition.edition_author_first.like("%{}%".format(champs["auteur"])))
        if "date" in champs:
            filtres.append(Edition.edition_cleanDate.like("%{}%".format(champs["date"])))
        if "place" in champs:
            filtres.append(Edition.edition_place2.like("%{}%".format(champs["place"])))
        if "pays" in champs:
            filtres.append(Edition.edition_country.like("%{}%".format(champs["pays"])))
        if "printer" in champs:
            filtres.append(Edition.edition_printer.like("%{}%".format(champs["printer"])))

        if "possesseur" in champs:
            joined.add(Edition.exemplaire)
            joined.add(Exemplaire.provenance)
            filtres.append(
                Provenance.provenance_possesseur_formeRejetee.like("%{}%".format(champs["possesseur"]))
            )
        if "begin_date" in champs and "end_date" in champs:
            filtres.append(Edition.edition_cleanDate.between(champs["begin_date"], champs["end_date"]))

        query = db.session.query(Edition)
        for join in joined:
            query = query.join(join)

        return query.filter(
            db.and_(*filtres)  # db.and_(*[x==1, y==2])  # db.and_(x==1, y==2)
        )

    @staticmethod
    def delete_edition(edition_id):
        """
        Fonction qui supprime la notice
        :param edition_id: l'identifiant de l'édition à récupérer dans l'adresse de la notice
        :type edition_id: int
        :returns : Booleens
        """
        # récupération de l'objet édition

        edition = Edition.query.get(edition_id)
        # récupération de toutes les citations liées avec cette édition
        citations=edition.citation
        # récupération de tous les exemplaires liés avec cette édition
        exemplars=edition.exemplaire
        # récupération de toutes les références liées avec cette édition
        refs=edition.reference

        # suppression de tous les exemplaires, citations et références liés avec une édition
        try:
            for cit in citations:
                db.session.delete(cit)
                db.session.commit()
            for exemp in exemplars:
                db.session.delete(exemp)
                db.session.commit()
            for ref in refs:
                db.session.delete(ref)
                db.session.commit()

            db.session.delete(edition)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False



class Bibliothecae(db.Model):
    bibliothecae_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    bibliothecae_library = db.Column(db.Text)
    bibliothecae_adresse = db.Column(db.Text)
    bibliothecae_ville = db.Column(db.Text)
    bibliothecae_pays = db.Column(db.Text)
    bibliothecae_web = db.Column(db.Text)
    exemplaire = db.relationship("Exemplaire", back_populates="bibliothecae")

    def ajout_bibliotheque(library, adresse, ville, pays, web):

        """On rajoute une bibliothèque
        :param library : nom de bibliothèque
        :param adresse: adresse de bibliothèque
        :param ville: ville
        :param pays: pays
        :param web: lien vers le site
        :type library, adresse, ville, pays, web: str
        :return : Booleen
        """
        bibliotheques = Bibliothecae(
            bibliothecae_library=library,
            bibliothecae_web=web,
            bibliothecae_adresse=adresse,
            bibliothecae_ville=ville,
            bibliothecae_pays=pays,

        )
        print(bibliotheques)
        try:

            db.session.add(bibliotheques)
            db.session.commit()


            return True, bibliotheques
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_bibliotheque(id, library, adresse, ville, pays, web):

        """
        On modifie les données sur bibliothèque
        :param id: l'identifiant de la bibliothèque
        :type id: int
        :param library : nom de bibliothèque
        :param adresse: adresse de bibliothèque
        :param ville: ville
        :param pays: pays
        :param web: lien vers le site
        :type library, adresse, ville, pays, web: str
        :return : Booleen 
        """
        bibliotheques = Bibliothecae.query.get(id)
        bibliotheques.bibliothecae_library=library,
        bibliotheques.bibliothecae_web = web,
        bibliotheques.bibliothecae_adresse = adresse,
        bibliotheques.bibliothecae_ville = ville,
        bibliotheques.bibliothecae_pays = pays,



        try:

            db.session.add(bibliotheques)
            db.session.commit()

            return True, bibliotheques
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_bibliotheque(bibliothecae_id):
        """
        Supprime une bibliothèque dans la base de données.
        :param bibliothecae_id : un identifiant d'une bibliothèque
        """

        bibliotheque = Bibliothecae.query.get(bibliothecae_id)

        try:

            db.session.delete(bibliotheque)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False




class Exemplaire(db.Model):
    exemplaire_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    exemplaire_pressmark = db.Column(db.Text)
    exemplaire_hauteur = db.Column(db.Text)
    exemplaire_variantesEdition = db.Column(db.Text)
    exemplaire_digitalURL = db.Column(db.Text)
    exemplaire_notes = db.Column(db.Text)
    exemplaire_provenances = db.Column(db.Text)
    exemplaire_locFingerprint = db.Column(db.Text)
    exemplaire_stcnFingerprint = db.Column(db.Text)
    exemplaire_annotationManuscrite = db.Column(db.Text)
    exemplaire_collator_etatMateriel = db.Column(db.Text)
    exemplaire_collator_largeur = db.Column(db.Text)
    exemplaire_reliure_recueilFactice = db.Column(db.Text)
    exemplaire_reliure_reliure  = db.Column(db.Text)
    exemplaire_reliure_reliureXVI = db.Column(db.Text)
    exemplaire_relieAvec = db.Column(db.Text)
    exemplaire_edition_id = db.Column(db.Integer, db.ForeignKey('edition.edition_id'))
    exemplaire_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    exemplaire_bibliothecae_id = db.Column(db.Text, db.ForeignKey('bibliothecae.bibliothecae_id'))
    edition = db.relationship("Edition", back_populates="exemplaire")
    bibliothecae = db.relationship("Bibliothecae", back_populates="exemplaire")
    provenance = db.relationship("Provenance", back_populates="exemplaire")
    user = db.relationship("User", back_populates="exemplaire")



    def ajout_exemplaire(pressmark, hauteur, variantesEdition, digitalURL, etatMateriel, notes, provenances, locFingerprint, stcnFingerprint, annotationManuscrite, largeur, recueilFactice, reliure, reliureXVI, relieAvec, edition_id, bibliothecae_id, user_id):

        """On rajoute un exemplaire pour édition
        :param pessmark : cote
        :param hauteur: hauteur d'exemplaire
        :param variantesEdition: variantes d'édition
        :param digitalURL: lien vers une numérisation
        :param etatMateriel: état matériel d'exemplaire
        :param notes : notes sur exemplaire
        :param provenances : provenance d'exemplaire
        :param locFingerprint : empreinte LOC
        :param stcnFingerprint : empreinte STCN
        :param annotationManuscrite : information sur annotation manuscrite
        :param largeur : largeur d'édition
        :param recueilFactice : receuil factice (oui/non)
        :param reliure : reliure d'exemplaire
        :param reliureXVI : reliure de XVI (oui/non)
        :param relieAvec : relation avec autre exemplaires/édition
        :param edition_id : identifiant de l'édition
        :param bibliothecae_id : identifiant de la bibliothèque
        :param user_id : identifiant de créateur de notice
        :type user_id, bibliothecae_id, edition_id : int
        :type pressmark, hauteur, variantesEdition, digitalURL, etatMateriel, notes, provenances, locFingerprint, stcnFingerprint, annotationManuscrite, largeur, recueilFactice, reliure, reliureXVI, relieAvec: str
        :return : Booleen
        """
        exemplars = Exemplaire(
            exemplaire_pressmark=pressmark,
            exemplaire_hauteur=hauteur,
            exemplaire_variantesEdition=variantesEdition,
            exemplaire_digitalURL=digitalURL,
            exemplaire_collator_etatMateriel=etatMateriel,
            exemplaire_notes=notes,
            exemplaire_provenances=provenances,
            exemplaire_locFingerprint=locFingerprint,
            exemplaire_stcnFingerprint=stcnFingerprint,
            exemplaire_annotationManuscrite=annotationManuscrite,
            exemplaire_collator_largeur=largeur,
            exemplaire_reliure_recueilFactice=recueilFactice,
            exemplaire_reliure_reliure=reliure,
            exemplaire_reliure_reliureXVI=reliureXVI,
            exemplaire_relieAvec = relieAvec,
            exemplaire_edition_id=edition_id,
            exemplaire_bibliothecae_id=bibliothecae_id if len(bibliothecae_id) > 0 else None,
            exemplaire_user_id = user_id
        )
        print(exemplars)
        try:

            db.session.add(exemplars)
            db.session.commit()


            return True, exemplars
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_exemplaire(id, pressmark, hauteur, variantesEdition, digitalURL, etatMateriel, notes, provenances, locFingerprint, stcnFingerprint, annotationManuscrite, largeur, recueilFactice, relieAvec, reliure, reliureXVI, bibliothecae_id, user_id):
        """On modifie un exemplaire
                :param id : identifiant d'exemplaire
                :param pessmark : cote
                :param hauteur: hauteur d'exemplaire
                :param variantesEdition: variantes d'édition
                :param digitalURL: lien vers une numérisation
                :param etatMateriel: état matériel d'exemplaire
                :param notes : notes sur exemplaire
                :param provenances : provenance d'exemplaire
                :param locFingerprint : empreinte LOC
                :param stcnFingerprint : empreinte STCN
                :param annotationManuscrite : information sur annotation manuscrite
                :param largeur : largeur d'édition
                :param recueilFactice : receuil factice (oui/non)
                :param reliure : reliure d'exemplaire
                :param reliureXVI : reliure de XVI (oui/non)
                :param relieAvec : relation avec autre exemplaires/édition
                :param edition_id : identifiant de l'édition
                :param bibliothecae_id : identifiant de la bibliothèque
                :param user_id : identifiant de créateur de notice
                :type id, user_id, bibliothecae_id, edition_id : int
                :type pressmark, hauteur, variantesEdition, digitalURL, etatMateriel, notes, provenances, locFingerprint, stcnFingerprint, annotationManuscrite, largeur, recueilFactice, reliure, reliureXVI, relieAvec: str
                :return : Booleen
                """
        exemplaires = Exemplaire.query.get(id)

        exemplaires.exemplaire_pressmark = pressmark,
        exemplaires.exemplaire_hauteur = hauteur,
        exemplaires.exemplaire_variantesEdition = variantesEdition,
        exemplaires.exemplaire_digitalURL = digitalURL,
        exemplaires.exemplaire_collator_etatMateriel = etatMateriel,
        exemplaires.exemplaire_notes = notes,
        exemplaires.exemplaire_provenances = provenances,
        exemplaires.exemplaire_locFingerprint = locFingerprint,
        exemplaires.exemplaire_stcnFingerprint = stcnFingerprint,
        exemplaires.exemplaire_annotationManuscrite = annotationManuscrite,
        exemplaires.exemplaire_collator_largeur = largeur,
        exemplaires.exemplaire_reliure_recueilFactice = recueilFactice,
        exemplaires.exemplaire_reliure_reliure = reliure,
        exemplaires.exemplaire_relieAvec = relieAvec,
        exemplaires.exemplaire_reliure_reliureXVI = reliureXVI,
        exemplaires.exemplaire_bibliothecae_id = bibliothecae_id,
        exemplaires.exemplaire_user_id = user_id

        try:
            db.session.add(exemplaires)
            db.session.commit()

            return True, exemplaires
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_exemplaire(exemplaire_id):
        """
        Supprime un exemplaire dans la base de données.
        :param exemplaire_id : identifiant d'un exemplaire
        :return : Booleen
        """

        exemplaire = Exemplaire.query.get(exemplaire_id)
        provs=exemplaire.provenance

        try:
            for prov in provs:
                db.session.delete(prov)
                db.session.commit()

            db.session.delete(exemplaire)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False


class Reference(db.Model):
    reference_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    reference_volume = db.Column(db.Text)
    reference_page = db.Column(db.Text)
    reference_recordNumber = db.Column(db.Text)
    reference_note = db.Column(db.Text)
    reference_bibliographie_id = db.Column(db.Integer, db.ForeignKey('bibliographie.bibliographie_id'))
    reference_edition_id = db.Column(db.Integer, db.ForeignKey('edition.edition_id'))
    edition = db.relationship("Edition", back_populates="reference")
    bibliographie = db.relationship("Bibliographie", back_populates="reference")

    def ajout_reference(volume, page, recordNumber, note, bibliographie_id, edition_id):
        """On rajoute une référence
                :param volume : volume d'un oeuvre
                :param page: page d'un oeuvre
                :param recordNumber: numéro d'enregistrement
                :param note: notes sur la référence
                :param bibliographie_id: identifiant d'un oeuvre
                :param edition_id : identifiant d'édition
                :type volume, page, recordNumber, note: str
                :type bibliographie_id, edition_id: int
                :return : Booleen
                """
        refs=Reference(

            reference_volume=volume,
            reference_page=page,
            reference_recordNumber=recordNumber,
            reference_note=note,
            reference_bibliographie_id=bibliographie_id if len(bibliographie_id) > 0 else None,
            reference_edition_id=edition_id,

        )
        print(refs)
        try:
             db.session.add(refs)
             db.session.commit()

             return True, refs
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_reference(id, volume, page, recordNumber, note, bibliographie_id):
        """On modifie une référence
            :param id: identifiant de le référence
            :param volume : volume d'un oeuvre
            :param page: page d'un oeuvre
            :param recordNumber: numéro d'enregistrement
            :param note: notes sur la référence
            :param bibliographie_id: identifiant d'un oeuvre
            :param edition_id : identifiant d'édition
            :type volume, page, recordNumber, note: str
            :type id, bibliographie_id, edition_id: int
            :return : Booleen
         """
        references = Reference.query.get(id)
        references.reference_volume = volume,
        references.reference_page = page,
        references.reference_recordNumber = recordNumber,
        references.reference_note = note,
        references.reference_bibliographie_id = bibliographie_id,


        print(references)
        try:
            db.session.add(references)
            db.session.commit()

            return True, references

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_reference(reference_id):
        """
        Supprime une référence dans la base de données.
        :param reference_id : un identifiant d'une référence
        :return : Booleen
        """

        reference = Reference.query.get(reference_id)

        try:

            db.session.delete(reference)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False


class Bibliographie(db.Model):
    bibliographie_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    bibliographie_code = db.Column(db.Text)
    bibliographie_author = db.Column(db.Text)
    bibliographie_bibliReference = db.Column(db.Text)
    bibliographie_title = db.Column(db.Text)
    bibliographie_imprint = db.Column(db.Text)
    bibliographie_URLLink = db.Column(db.Text)
    reference = db.relationship("Reference", back_populates="bibliographie")

    def ajout_bibliographie(code, author, bibliReference, title, imprint, urlLink):
        """On rajoute un oeuvre
                  :param code : code d'un oeuvre
                  :param bibliReference: référence bibliographique
                  :param title: titre d'un oeuvre
                  :param imprint: imprint
                  :param urlLink: lien vers une numérisation
                  :param edition_id : identifiant d'édition
                  :type code, author, bibliReference, title, imprint, urlLink: str
                  :return : Booleen
                """
        bibliographia=Bibliographie(
            bibliographie_code=code,
            bibliographie_author=author,
            bibliographie_bibliReference=bibliReference,
            bibliographie_title=title,
            bibliographie_imprint=imprint,
            bibliographie_URLLink=urlLink,
        )

        print(bibliographia)
        try:

            db.session.add(bibliographia)
            db.session.commit()

            return True, bibliographia
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_bibliographie(id, code, author, bibliReference, title, imprint, urlLink):
        """On modifie un oeuvre
          :param id: identifiant d'un oeuvre
          :param code : code d'un oeuvre
          :param bibliReference: référence bibliographique
          :param title: titre d'un oeuvre
          :param imprint: imprint
          :param urlLink: lien vers une numérisation
          :param edition_id : identifiant d'édition
          :type volume, page, recordNumber, note: str
          :type id : int
          :type code, author, bibliReference, title, imprint, urlLink : str
          :return : Booleen
        """
        bibliographies = Bibliographie.query.get(id)
        bibliographies.bibliographie_code = code,
        bibliographies.bibliographie_author = author,
        bibliographies.bibliographie_bibliReference = bibliReference,
        bibliographies.bibliographie_title = title,
        bibliographies.bibliographie_imprint = imprint,
        bibliographies.bibliographie_URLLink = urlLink,

        print(bibliographies)
        try:
            db.session.add(bibliographies)
            db.session.commit()

            return True, bibliographies

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_bibliographie(bibliographie_id):
        """
        Supprime un oeuvre et toutes les références associées
        :param bibliographie_id : un identifiant d'un oeuvre
        :return : Booleen
        """
        bibliographie = Bibliographie.query.get(bibliographie_id)
        # on récupere toutes ls références associées
        refs=bibliographie.reference
        # on supprime  toutes les références associées
        try:
            for ref in refs:
                db.session.delete(ref)
                db.session.commit()

            db.session.delete(bibliographie)
            db.session.commit()
            return True

        except Exception as failed:
            print(failed)
            return False



class Citation(db.Model):
    citation_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    citation_dbnumber = db.Column(db.Integer)
    citation_url = db.Column(db.Text)
    citation_edition_id = db.Column(db.Integer, db.ForeignKey('edition.edition_id'))
    citation_catalogue_id = db.Column(db.Integer, db.ForeignKey('catalogue.catalogue_id'))
    edition = db.relationship("Edition", back_populates="citation")
    catalogue = db.relationship("Catalogue", back_populates="citation")

    def ajout_citation(dbnumber, url, edition_id, catalogue_id):
        """On rajoute une citation
         :param dbnumber : numéro dans la base
         :param url: lien vers une version numérisée
         :param catalogue_id: identifiant d'un catalogue
         :type url: str
         :type dbnumber, catalogue_id : int
         :return : Booleen
         """
        citations=Citation(
            citation_dbnumber=dbnumber,
            citation_url=url,
            citation_edition_id=edition_id,
            citation_catalogue_id=catalogue_id if len(catalogue_id) > 0 else None,
        )
        print(citations)
        try:
            db.session.add(citations)
            db.session.commit()

            return True, citations
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_citation(id, dbnumber, url, catalogue_id):
        """On modifie une citation
         :param id: identifiant d'une citation
         :param dbnumber : numéro dans la base
         :param url: lien vers une version numérisée
         :param catalogue_id: identifiant d'un catalogue
         :type url: str
         :type id, dbnumber, catalogue_id : int
         :return : Booleen
         """
        citations = Citation.query.get(id)
        citations.citation_dbnumber = dbnumber,
        citations.citation_url = url,
        citations.citation_catalogue_id=catalogue_id,

        print(citations)
        try:
            db.session.add(citations)
            db.session.commit()

            return True, citations

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_citation(citation_id):
        """
        On supprime une citation
        :param citation_id : un identifiant d'une citation
        :return : Booleen
        """

        citation = Citation.query.get(citation_id)


        try:

            db.session.delete(citation)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False


class Digital(db.Model):
    digital_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    digital_url = db.Column(db.Text)
    digital_provider = db.Column(db.Text, nullable=False)
    digital_edition_id = db.Column(db.Integer, db.ForeignKey('edition.edition_id'))
    edition = db.relationship("Edition", back_populates="digital")


class Provenance(db.Model):
    provenance_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    provenance_exLibris = db.Column(db.Text)
    provenance_exDono = db.Column(db.Text)
    provenance_envoi = db.Column(db.Text)
    provenance_notesManuscrites = db.Column(db.Text)
    provenance_armesPeintes = db.Column(db.Text)
    provenance_restitue = db.Column(db.Text)
    provenance_mentionEntree = db.Column(db.Text)
    provenance_estampillesCachets = db.Column(db.Text)
    provenance_reliure_provenance=db.Column(db.Text)
    provenance_possesseur = db.Column(db.Text)
    provenance_possesseur_formeRejetee = db.Column(db.Text)
    provenance_notes = db.Column(db.Text)
    provenance_exemplaire_id = db.Column(db.Integer, db.ForeignKey('exemplaire.exemplaire_id'))
    exemplaire = db.relationship("Exemplaire", back_populates="provenance")

    def ajout_provenance(exlibris, exdono, envoi, notesManuscrites, armesPeintes, restitue, mentionEntree, estampillesCachets, possesseur, possesseur_formeRejetee, notes, reliure_provenance, exemplaire_id):
        """On ajoute une provenance
        :param exlibris : données sur ex-Libris
        :param exdono: données sur ex-Dono
        :param envoi: données sur envoi
        :param notesManuscrites : notes manuscrites sur provenance
        :param armesPeintes : données sur armes et peintes
        :param mentionEntree : mention d'entrée
        :param estampillesCachets : estampilles et cachets
        :param possesseur : nom de possesseur
        :param possesseur_formeRejetee : formes rejétées du nom de possesseur
        :param notes : notes sur provenance
        :param reliure_provenance : provenance de reliure
        :param restitue : provenance restituée
        :param exemplaire_id : identifiant d'exemplaire
        :type exlibris, exdono, envoi, notesManuscrites, armesPeintes, restitue, mentionEntree, estampillesCachets, possesseur, possesseur_formeRejetee, notes, reliure_provenance: str
        :type exemplaire_id : int
        :return : Booleen
        """
        provenances=Provenance(
             provenance_exLibris = exlibris,
             provenance_exDono = exdono,
             provenance_envoi = envoi,
             provenance_notesManuscrites = notesManuscrites,
             provenance_armesPeintes = armesPeintes,
             provenance_restitue = restitue,
             provenance_mentionEntree = mentionEntree,
             provenance_estampillesCachets = estampillesCachets,
             provenance_possesseur = possesseur,
             provenance_reliure_provenance=reliure_provenance,
             provenance_possesseur_formeRejetee = possesseur_formeRejetee,
             provenance_notes = notes,
             provenance_exemplaire_id = exemplaire_id

         )
        print(provenances)
        try:
            db.session.add(provenances)
            db.session.commit()

            return True, provenances

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_provenance(id, exlibris, exdono, envoi, notesManuscrites, armesPeintes, restitue, mentionEntree, estampillesCachets, possesseur, possesseur_formeRejetee, reliure_provenance, notes):

        """On modifie une provenance
        :param id : identifiant de provenance
        :param exlibris : données sur ex-Libris
        :param exdono: données sur ex-Dono
        :param envoi: données sur envoi
        :param notesManuscrites : notes manuscrites sur provenance
        :param armesPeintes : données sur armes et peintes
        :param mentionEntree : mention d'entrée
        :param estampillesCachets : estampilles et cachets
        :param possesseur : nom de possesseur
        :param possesseur_formeRejetee : formes rejétées du nom de possesseur
        :param notes : notes sur provenance
        :param reliure_provenance : provenance de reliure
        :param restitue : provenance restituée
        :param exemplaire_id : identifiant d'exemplaire
        :type exlibris, exdono, envoi, notesManuscrites, armesPeintes, restitue, mentionEntree, estampillesCachets, possesseur, possesseur_formeRejetee, notes, reliure_provenance: str
        :type id, exemplaire_id : int
        :return : Booleen
        """
        provenances = Provenance.query.get(id)


        provenances.provenance_exLibris = exlibris,
        provenances.provenance_exDono = exdono,
        provenances.provenance_envoi = envoi,
        provenances.provenance_notesManuscrites = notesManuscrites,
        provenances.provenance_armesPeintes = armesPeintes,
        provenances.provenance_restitue = restitue,
        provenances.provenance_mentionEntree = mentionEntree,
        provenances.provenance_estampillesCachets = estampillesCachets,
        provenances.provenance_reliure_provenance=reliure_provenance,
        provenances.provenance_possesseur = possesseur,
        provenances.provenance_possesseur_formeRejetee = possesseur_formeRejetee,
        provenances.provenance_notes = notes,


        print(provenances)
        try:
            db.session.add(provenances)
            db.session.commit()

            return True, provenances

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_provenance(provenance_id):
        """
        On supprime une provenance
        :param provenance_id : un identifiant d'une provenance
        :return : Booleen
        """

        provenance = Provenance.query.get(provenance_id)

        try:

            db.session.delete(provenance)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False


class Catalogue(db.Model):
    catalogue_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    catalogue_nom = db.Column(db.Text)
    catalogue_nom_abrege = db.Column(db.Text)
    catalogue_site = db.Column(db.Text)
    citation = db.relationship("Citation", back_populates="catalogue")

    def ajout_catalogue(nom, nom_abrege, site):
        """On ajoute une provenance
        :param nom : nom de catalogue
        :param nom_abrege: nom abrégé de catalogue
        :param site: lien vers le site
        :type nom, nom_abrege, site: str
        :return : Booleen
        """
        catalogue=Catalogue(
            catalogue_nom=nom,
            catalogue_nom_abrege=nom_abrege,
            catalogue_site=site,

        )

        print(catalogue)
        try:

            db.session.add(catalogue)
            db.session.commit()

            return True, catalogue
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def modif_catalogue(id, nom, nom_abrege, site):
        """On modifie une provenance
            :param id : identifiant de catalogue
            :param nom : nom de catalogue
            :param nom_abrege: nom abrégé de catalogue
            :param site: lien vers le site
            :type nom, nom_abrege, site: str
            :type id : int
            :return : Booleen
            """
        catalogues = Catalogue.query.get(id)
        catalogues.catalogue_nom = nom,
        catalogues.catalogue_nom_abrege = nom_abrege,
        catalogues.catalogue_site = site,


        print(catalogues)
        try:
            db.session.add(catalogues)
            db.session.commit()

            return True, catalogues

        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def delete_catalogue(catalogue_id):
        """
        On supprime un catalogue
        :param catalogue_id : un identifiant d'un catalogue
        :return : Booleen
        """

        catalogue = Catalogue.query.get(catalogue_id)

        try:

            db.session.delete(catalogue)
            db.session.commit()
            return True
        except Exception as failed:
            print(failed)
            return False