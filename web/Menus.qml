import FlatSiteBuilder 2.0

Menus {
    Menu {
        name: 'default_de'
        Menuitem {
            title: 'Home'
            url: '#wrapper'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Slides'
            url: '#slides'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Portfolio'
            url: '#portfolio'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'FAQ'
            url: '#faq'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Downloads'
            url: '#downloads'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Kontakt'
            url: '#contact'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Deutsch'
            url: '#'
            icon: 'assets/images/flags/de.png'
            attributes: ''
            Menuitem {
                title: '[US] English'
                url: 'index.html'
                icon: 'assets/images/flags/us.png'
            }
            Menuitem {
                title: 'Deutsch'
                url: '#'
                icon: 'assets/images/flags/de.png'
            }
        }
    }
    Menu {
        name: 'default'
        Menuitem {
            title: 'Home'
            url: '#wrapper'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Slides'
            url: '#slides'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Portfolio'
            url: '#portfolio'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'FAQ'
            url: '#faq'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Downloads'
            url: '#downloads'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'Contact'
            url: '#contact'
            icon: ''
            attributes: ''
        }
        Menuitem {
            title: 'English'
            url: '#'
            icon: 'assets/images/flags/us.png'
            attributes: ''
            Menuitem {
                title: '[US] English'
                url: '#'
                icon: 'assets/images/flags/us.png'
            }
            Menuitem {
                title: 'Deutsch'
                url: 'index_de.html'
                icon: 'assets/images/flags/de.png'
            }
        }
    }
}
