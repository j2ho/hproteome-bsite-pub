# HProteome-BSite

**Public repository showcasing the source code for the [HProteome-BSite database](https://galaxy.seoklab.org/hproteome-bsite/database/).**

## Project

**Visit the live database**: [https://galaxy.seoklab.org/hproteome-bsite/database/](https://galaxy.seoklab.org/hproteome-bsite/database/)

![HProteome-BSite Interface](assets/mainpage.png)
*Screenshot of the HProteome-BSite web interface*

## 📋 Project Overview

HProteome-BSite is a comprehensive database and web interface for exploring human-proteome-wide binding site and ligand information. This repository showcases the Django-based web application source code that powers the database interface. 

### Key Features
- **Comprehensive Database**: Proteome-wide binding site information with over 20,000+ protein domains
- **Interactive Web Interface**: User-friendly search and visualization with molecular structure viewing
- **Django Framework**: Robust web application architecture with SQLite database
- **Molecular Visualization**: Integration with MolStar for 3D structure viewing
- **Bulk Download**: Comprehensive data export capabilities


### Binding Site Prediction Tool: GalaxySite2
- Provided predictions of binding sites and ligands were made using GalaxySite, a template based binding site prediction
method. Upon building HProteome-BSite, I have updated GalaxySite both database- and algorithm-wise. 
- Outline of GalaxySite binding prediction on the AlphaFold human structure database. Details of this method can be found in the paper cited at the end. 
![Binding Site Prediction Pipeline](assets/algorithm.png)


### Technologies Used
- **Backend**: Python, Django 4.0.5
- **Database**: SQLite3
- **Frontend**: HTML, CSS, JavaScript, MolStar
- **Deployment**: WSGI application server

## 📁 Repository Structure

```
hproteome-bsite-pub/
├── database/                   # Main Django application
│   ├── models.py              # Database models and schema
│   ├── views.py               # Application views and logic
│   ├── urls.py                # URL routing
│   ├── templates/             # HTML templates
│   └── migrations/            # Database migration files
├── sitedb/                    # Django project configuration
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py               # WSGI application entry point
└── manage.py                 # Django management 
```

## ⚠️ Repository Notes

This is a **showcase repository** containing the core source code. Please note:

- **Static files excluded**: Production static files (CSS, JS, images) are not included
- **Security files removed**: Sensitive configuration and credentials have been removed
- **Live deployment**: The fully functional version is available at the link above
- **Data files**: Actual predictions (PDB files for complex structures) are excluded

## Contact

For questions about the HProteome-BSite database, please visit the [official website](https://galaxy.seoklab.org/hproteome-bsite/database/).

## Citation

If you use HProteome-BSite in your research, please cite:

**Paper**: [HProteome-BSite: A comprehensive database of human proteome-wide binding sites](https://doi.org/10.1093/nar/gkac873)

**Website**: [https://galaxy.seoklab.org/hproteome-bsite/database/](https://galaxy.seoklab.org/hproteome-bsite/database/)

```bibtex
@article{hproteome_bsite_2022,
    title={HProteome-BSite: A comprehensive database of human proteome-wide binding sites},
    author={Jiho Sim, Sohee Kwon, Chaok Seok*},
    journal={Nucleic Acids Research},
    year={2022},
    doi={10.1093/nar/gkac873}
}
```

---

**Note**: This repository contains the core source code only. For the full functionality of the HProteome-BSite database, additional configuration and static files are required. 
