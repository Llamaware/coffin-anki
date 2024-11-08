# coffin-anki

A script to generate Anki decks from Coffin of Andy and Leyley translations.

[!screenshot](/screenshot.png)

---

## Usage

Place the `dialogue.csv` of your desired language in the same directory as the script.

Then run `python gen-anki.py`

`output.csv` will be generated in this format: `sort_number` | `tl_expression` | `en_meaning` | `TlName` | `EnName`

Then import the `.csv` file into Anki. You can use the below template, or create your own.

---

## Sample decks

Some premade decks may be available from the releases.

Front Template:

```
<div class="tag">
	TCAL{{#Tags}} | {{/Tags}}{{Tags}}  {{#JaName}} | {{/JaName}}{{JaName}} {{#EnName}} | {{/EnName}}{{EnName}}
</div>

{{^Reverse}}
	<div class="japanese">
		{{Expression}}
	</div>
{{/Reverse}}

{{#Reverse}}
	<div class="japanese">
		{{Expression}}
	</div>
{{/Reverse}}
```

Back Template:

```
{{FrontSide}}
<hr id=answer>

<div class="meaning">
 	{{furigana:Meaning}}
</div>
```

Styling:

```
@font-face {
  font-family: "Yu Mincho";
  src: url("_yumin.ttf") ;
}
@font-face {
  font-family: "Yu Mincho DemiBold";
  src: url("_yumindb.ttf") ;
}
.card {
 font-family:Yu Mincho;
 font-size: 22px;
 background-color:#FFFAF0;
 text-align: left;
 color:#333;
}

.tag {
  color:#585858; 
  font-size: 20px
}

.japanese {
  font-size: 35px;
}
.meaning {
  margin-top: 36px;
  font-size: 22px;
}

b {
  font-family: "Yu Mincho DemiBold";
  color:#000;
}
```

---

CSS and inspiration from [steins;gate anki](https://github.com/asakura42/steins-gate-anki)