import FlatSiteBuilder 1.0
import TextEditor 1.0
import MarkdownEditor 1.0

Content {
    title: "Test"
    menu: "default"
    layout: "default"
    date: "2023-01-16"

    Section {

        Row {

            Column {
                span: 12

                Text {
                    text: "Item
{
	Text
	{
		text: &quot;Hello world&quot;
	}
}"
                }

                Markdown {
                    text: "## Test

Ipsum dolor"
                }
            }
        }
    }
}
