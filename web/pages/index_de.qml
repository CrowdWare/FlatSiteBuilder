import FlatSiteBuilder 2.0
import RevolutionSlider 1.0
import TextEditor 1.0
import ImageEditor 1.0

Content {
    title: "Index"
    menu: "default_de"
    author: "admin"
    layout: "default"
    date: "2023-01-20"
    language: "de"

    Section {
        fullwidth: true

        RevolutionSlider {

            Slide {
                src: "E:/SourceCode/FlatSiteBuilder/web/assets/images/tagcloud.png"
            }
        }
    }

    Section {

        Row {

            Column {
                span: 12

                Text {
                    text: "&lt;!-- welcome --&gt;
&lt;h1&gt;
	&lt;strong&gt;Willkommen&lt;/strong&gt; bei {{ site.title }}
&lt;/h1&gt;
&lt;p class=&quot;lead&quot;&gt;Wussten Sie, dass Sie Ihre Projekt-Website kostenlos auf Github-Pages hosten können?&lt;/p&gt;
&lt;p class=&quot;lead&quot;&gt;
Der FlatSiteBuilder ist ein sehr einfach zu verwendendes Content-Management-System (CMS) und ein Werkzeug zur Erstellung von Inhalten, das als Desktop-Anwendung unter Linux und Windows ausgeführt wird. 
Sie können Webinhalte erstellen, die Sie kostenlos auf Github-Pages oder bei einem anderen Anbieter hosten können. 
Da alle Seiten auf dem Desktop erstellt werden, ist es das schnellste Content-Management-System, das verfügbar ist. 
Es wird kein Code auf dem Webserver ausgeführt.
&lt;/p&gt;"
                    adminlabel: "Willkommen"
                }
            }
        }

        Row {

            Column {
                span: 12

                Text {
                    text: "&lt;div class=&quot;divider styleColor&quot;/&gt;"
                    adminlabel: "divider"
                }
            }
        }

        Row {

            Column {
                span: 4

                Image {
                    src: "Dashboard.png"
                }
            }

            Column {
                span: 8

                Text {
                    text: "&lt;h3&gt;&lt;strong&gt;FlatSiteBuilder&lt;/strong&gt;&lt;/h3&gt;
&lt;p class=&quot;lead&quot;&gt;
Der FlatSiteBuilder ist ein sehr einfach zu verwendendes Content-Management-System und ein Werkzeug zur Erstellung von Inhalten, das als Desktop-Anwendung auf Windows und Linux ausgeführt wird.
&lt;/p&gt;
"
                    adminlabel: "FlatSiteBuilder"
                }
            }
        }

        Row {

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;featured-box nobg border-only&quot;&gt;
	&lt;div class=&quot;box-content&quot;&gt;
		&lt;i class=&quot;fa fa-thumbs-up&quot;&gt;&lt;/i&gt;
		&lt;h4&gt;Schnellstes CMS&lt;/h4&gt;
		&lt;p&gt;Aufgrund der Tatsache, dass der FlatSiteBuilder nur flache HTML-Dateien erstellt, ist es somit das schnellste CMS, das verfügbar ist.&lt;/p&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "Fatest CMS"
                }
            }

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;featured-box nobg border-only&quot;&gt;
	&lt;div class=&quot;box-content&quot;&gt;
		&lt;i class=&quot;fa fa-thumbs-up&quot;&gt;&lt;/i&gt;
		&lt;h4&gt;Easiest CMS&lt;/h4&gt;
		&lt;p&gt;Aufgrund der Tatsache, dass FlatSiteBuilder auf dem Desktop ausgeführt wird, ist es somit eines der einfachsten zu verwendenden CMS, die verfügbar sind.&lt;/p&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "Easiest"
                }
            }

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;featured-box nobg border-only&quot;&gt;
	&lt;div class=&quot;box-content&quot;&gt;
		&lt;i class=&quot;fa fa-thumbs-up&quot;&gt;&lt;/i&gt;
		&lt;h4&gt;Safest CMS&lt;/h4&gt;
		&lt;p&gt;Aufgrund der Tatsache, dass wir Github als Versionskontrolle für den Inhalt verwenden, ist FlatSiteBuilder somit das sicherste CMS, das verfügbar ist.&lt;/p&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "Safest"
                }
            }

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;featured-box nobg border-only&quot;&gt;
	&lt;div class=&quot;box-content&quot;&gt;
		&lt;i class=&quot;fa fa-thumbs-up&quot;&gt;&lt;/i&gt;
		&lt;h4&gt;Cheapest CMS&lt;/h4&gt;
		&lt;p&gt;Aufgrund der Tatsache, dass das Hosting auf Github-Seiten kostenlos ist, ist FlatSiteBuilder somit das günstigste CMS, das verfügbar ist.&lt;/p&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "Cheapest"
                }
            }
        }

        Row {

            Column {
                span: 12

                Text {
                    text: "&lt;div class=&quot;divider styleColor&quot;/&gt;"
                    adminlabel: "divider"
                }
            }
        }
    }

    Section {
        id:  slides

        Row {

            Column {
                span: 4

                Text {
                    text: "&lt;h3&gt;&lt;strong&gt;Vorschau&lt;/strong&gt;&lt;/h3&gt;
&lt;p class=&quot;lead&quot;&gt;
Hier sind Beispiel-Vorschau-Bilder von FlatSiteBuilder in Aktion.&lt;/p&gt;"
                    adminlabel: "Preview"
                }
            }

            Column {
                span: 8

                Text {
                    text: "&lt;div class=&quot;owl-carousel controlls-over&quot; data-plugin-options=&#x27;{&quot;items&quot;: 1, &quot;singleItem&quot;: true, &quot;navigation&quot;: false, &quot;pagination&quot;: false, &quot;transitionStyle&quot;:&quot;fadeUp&quot;, &quot;autoPlay&quot;: true}&#x27;&gt;
	&lt;div&gt;
		&lt;img alt=&quot;&quot; class=&quot;img-responsive&quot; src=&quot;assets/images/Editor.png&quot;&gt;
	&lt;/div&gt;
	&lt;div&gt;
		&lt;img alt=&quot;&quot; class=&quot;img-responsive&quot; src=&quot;assets/images/Layout.png&quot;&gt;
	&lt;/div&gt;
	&lt;div&gt;
		&lt;img alt=&quot;&quot; class=&quot;img-responsive&quot; src=&quot;assets/images/Columns.png&quot;&gt;
	&lt;/div&gt;
	&lt;div&gt;
		&lt;img alt=&quot;&quot; class=&quot;img-responsive&quot; src=&quot;assets/images/Modules.png&quot;&gt;
	&lt;/div&gt;
&lt;/div&gt;
"
                    adminlabel: "Slider"
                }
            }
        }
    }

    Section {
        id:  portfolio

        Row {

            Column {
                span: 12

                Text {
                    text: "&lt;div class=&quot;divider styleColor&quot;&gt;&lt;/div&gt;
&lt;h3&gt;&lt;strong&gt;Portfolio&lt;/strong&gt;&lt;/h3&gt;
&lt;p class=&quot;lead&quot;&gt;Hier können Sie einige Seiten sehen, die mit dem FlatSiteBuilder erstellt wurden.&lt;/p&gt;"
                    adminlabel: "Portfolio"
                }
            }
        }

        Row {

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;item-box&quot;&gt;
	&lt;figure&gt;
		&lt;a class=&quot;item-hover&quot; href=&quot;https://crowdware.github.io/web/&quot;&gt;
			&lt;span class=&quot;overlay color2&quot;&gt;&lt;/span&gt;
			&lt;span class=&quot;inner&quot;&gt;
				&lt;span class=&quot;block fa fa-plus fsize20&quot;&gt;&lt;/span&gt;
				&lt;strong&gt;PROJECT&lt;/strong&gt; DETAIL
			&lt;/span&gt;
		&lt;/a&gt;
		&lt;img class=&quot;img-responsive&quot; src=&quot;assets/images/crowdware.png&quot; width=&quot;260&quot; height=&quot;260&quot; alt=&quot;&quot;&gt;
	&lt;/figure&gt;
	&lt;div class=&quot;item-box-desc&quot;&gt;
		&lt;h4&gt;CrowdWare&lt;/h4&gt;
		&lt;small class=&quot;styleColor&quot;&gt;2017&lt;/small&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "CrowdWare"
                }
            }

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;item-box&quot;&gt;
	&lt;figure&gt;
		&lt;a class=&quot;item-hover&quot; href=&quot;https://artanidos.github.io/artananda/&quot;&gt;
			&lt;span class=&quot;overlay color2&quot;&gt;&lt;/span&gt;
			&lt;span class=&quot;inner&quot;&gt;
				&lt;span class=&quot;block fa fa-plus fsize20&quot;&gt;&lt;/span&gt;
				&lt;strong&gt;PROJECT&lt;/strong&gt; DETAIL
			&lt;/span&gt;
		&lt;/a&gt;
		&lt;img class=&quot;img-responsive&quot; src=&quot;assets/images/artananda.png&quot; width=&quot;260&quot; height=&quot;260&quot; alt=&quot;&quot;&gt;
	&lt;/figure&gt;
	&lt;div class=&quot;item-box-desc&quot;&gt;
		&lt;h4&gt;Artananda&lt;/h4&gt;
		&lt;small class=&quot;styleColor&quot;&gt;2017&lt;/small&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "Artananda"
                }
            }

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;item-box&quot;&gt;
	&lt;figure&gt;
		&lt;a class=&quot;item-hover&quot; href=&quot;https://artanidos.github.io/AnimationMaker/&quot;&gt;
			&lt;span class=&quot;overlay color2&quot;&gt;&lt;/span&gt;
			&lt;span class=&quot;inner&quot;&gt;
				&lt;span class=&quot;block fa fa-plus fsize20&quot;&gt;&lt;/span&gt;
				&lt;strong&gt;PROJECT&lt;/strong&gt; DETAIL
			&lt;/span&gt;
		&lt;/a&gt;
		&lt;img class=&quot;img-responsive&quot; src=&quot;assets/images/animationmaker.png&quot; width=&quot;260&quot; height=&quot;260&quot; alt=&quot;&quot;&gt;
	&lt;/figure&gt;
	&lt;div class=&quot;item-box-desc&quot;&gt;
		&lt;h4&gt;AnimationMaker&lt;/h4&gt;
		&lt;small class=&quot;styleColor&quot;&gt;2017&lt;/small&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "AnimationMaker"
                }
            }

            Column {
                span: 3

                Text {
                    text: "&lt;div class=&quot;item-box&quot;&gt;
	&lt;figure&gt;
		&lt;a class=&quot;item-hover&quot; href=&quot;https://crowdware.github.io/nrg/&quot;&gt;
			&lt;span class=&quot;overlay color2&quot;&gt;&lt;/span&gt;
			&lt;span class=&quot;inner&quot;&gt;
				&lt;span class=&quot;block fa fa-plus fsize20&quot;&gt;&lt;/span&gt;
				&lt;strong&gt;PROJECT&lt;/strong&gt; DETAIL
			&lt;/span&gt;
		&lt;/a&gt;
		&lt;img class=&quot;img-responsive&quot; src=&quot;assets/images/nrg.png&quot; width=&quot;260&quot; height=&quot;260&quot; alt=&quot;&quot;&gt;
	&lt;/figure&gt;
	&lt;div class=&quot;item-box-desc&quot;&gt;
		&lt;h4&gt;NRG-Exchange&lt;/h4&gt;
		&lt;small class=&quot;styleColor&quot;&gt;2017&lt;/small&gt;
	&lt;/div&gt;
&lt;/div&gt;"
                    adminlabel: "NRG"
                }
            }
        }
    }

    Section {
        id:  faq

        Row {

            Column {
                span: 12

                Text {
                    text: "&lt;div class=&quot;divider styleColor&quot;&gt;&lt;/div&gt;
&lt;h3&gt;&lt;strong&gt;FAQ&lt;/strong&gt;&lt;/h3&gt;"
                    adminlabel: "FAQ"
                }
            }
        }

        Row {
            cssclass: "featured-box-minimal margin-bottom30"

            Column {
                span: 4

                Text {
                    text: "&lt;h4&gt;&lt;i class=&quot;fa fa-question&quot;&gt;&lt;/i&gt; Wo kann ich meine Website hosten?
&lt;/4&gt;
&lt;p&gt; 
Sie können Ihre Website bei jedem Hosting-Provider hosten. 
Wir empfehlen Ihnen, Ihre Website bei 
&lt;a href=&quot;https://pages.github.com/&quot;&gt;github-pages&lt;/a&gt; zu hosten, 
da es kostenlos ist.&lt;/p&gt;
      "
                }
            }

            Column {
                span: 4

                Text {
                    text: "&lt;h4&gt;&lt;i class=&quot;fa fa-question&quot;&gt;&lt;/i&gt; Wie kann ich dynamischen Inhalt integrieren? 
&lt;/4&gt;
&lt;p&gt;
Sie können Dienste wie &lt;a href=&quot;https://disqus.com/&quot;&gt;disqus
&lt;/a&gt; verwenden, um z.B. Kommentare für Ihre Blog-Posts zu integrieren. 
Wir verwenden auch disqus, siehe unten unter Kommentare.&lt;/p&gt;"
                }
            }

            Column {
                span: 4
            }
        }
    }

    Section {
        id:  downloads

        Row {

            Column {
                span: 12

                Text {
                    text: "&lt;div class=&quot;divider styleColor&quot;&gt;&lt;/div&gt; "
                }
            }
        }

        Row {

            Column {
                span: 8

                Text {
                    text: "
&lt;h3&gt;&lt;strong&gt;Downloads&lt;/strong&gt;&lt;/h3&gt; 
&lt;p class=&quot;lead&quot;&gt;Hier kannst Du das letzte Release runterladen: &lt;a href=&quot;https://github.com/CrowdWare/FlatSiteBuilder/releases&quot;&gt;&lt;img src=&quot;assets/images/download.png&quot;&gt;&lt;/a&gt;&lt;/p&gt;
"
                    adminlabel: "Downloads"
                }
            }

            Column {
                span: 4

                Text {
                    text: "&lt;a href=&quot;https://www.producthunt.com/posts/flatsitebuilder?utm_source=badge-featured&amp;utm_medium=badge&amp;utm_souce=badge-flatsitebuilder&quot; target=&quot;_blank&quot;&gt;&lt;img src=&quot;https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=377562&amp;theme=neutral&quot; alt=&quot;FlatSiteBuilder - FSB&amp;#0032;is&amp;#0032;a&amp;#0032;easy&amp;#0032;to&amp;#0032;use&amp;#0032;content&amp;#0032;creation&amp;#0032;tool&amp;#0032;for&amp;#0032;the&amp;#0032;desktop | Product Hunt&quot; style=&quot;width: 250px; height: 54px;&quot; width=&quot;250&quot; height=&quot;54&quot; /&gt;&lt;/a&gt;"
                }
            }
        }
    }

    Section {

        Row {

            Column {
                span: 12

                Text {
                    text: "&lt;div class=&quot;divider styleColor&quot;&gt;&lt;/div&gt;
&lt;h3&gt;&lt;strong&gt;Kommentare&lt;/strong&gt;&lt;/h3&gt;
&lt;div id=&quot;disqus_thread&quot;&gt;&lt;/div&gt;
&lt;script&gt;
/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
/*
var disqus_config = function () {
this.page.url = &quot;{{ page.url }}&quot;;  
this.page.identifier = &quot;{{ page.title }}&quot;;
};
*/
(function() { // DON&#x27;T EDIT BELOW THIS LINE
var d = document, s = d.createElement(&#x27;script&#x27;);
s.src = &#x27;https://flatsitebuilder.disqus.com/embed.js&#x27;;
s.setAttribute(&#x27;data-timestamp&#x27;, +new Date());
(d.head || d.body).appendChild(s);
})();
&lt;/script&gt;
&lt;noscript&gt;Please enable JavaScript to view the &lt;a href=&quot;https://disqus.com/?ref_noscript&quot;&gt;comments powered by Disqus.&lt;/a&gt;&lt;/noscript&gt;"
                }
            }
        }
    }
}
