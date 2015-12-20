<svg  xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
	  width="210mm" height="{{ doc_height }}mm" viewBox="0 0 210mm {{ doc_height }}mm" streamable="true"
	  version="1.2"
	  >
	<style type="text/css">
		<![CDATA[
		rect.label-border{fill:none;stroke:navy;stroke-opacity:1;stroke-width:0.5mm;}

		svg.label.black rect.label-border{stroke:dimgrey;}
		svg.label.black foreignObject.header h1{color:dimgrey;}
		svg.label.red rect.label-border{stroke:maroon;}
		svg.label.red foreignObject.header h1{color:maroon;}
		svg.label.infusion rect.label-border{stroke:LightSeaGreen;}
		svg.label.infusion foreignObject.header h1{color:LightSeaGreen;}
		svg.label.green rect.label-border{stroke:ForestGreen;}
		svg.label.green foreignObject.header h1{color:ForestGreen;}
		svg.label.smoked rect.label-border{stroke:peru;}
		svg.label.smoked foreignObject.header h1{color:peru;}

		text.title{font-size:16px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.origin{font-size:14px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.type{font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.duration{font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.temp{text-anchor:middle;font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans;width:10mm;color:white;}

		foreignObject.header{font-style:normal;font-weight:normal;}
		foreignObject p{text-align:center;margin:0;}
		foreignObject.header h1,foreignObject.header h2,foreignObject.header h3{margin:0;padding:0;font-style:normal;font-weight:normal;text-align:center;}

		foreignObject.header h1{font-size:16px;}
		foreignObject.header h2{font-size:14px;margin-top:2mm;}
		foreignObject.header h3{font-size:12px;margin-top:2mm;}
		foreignObject.header p.ingredients{font-size:11px;margin-top:4mm;}
		]]>
	</style>
	{% for label in labels %}
	<svg x="{{ label.x }}mm" y="{{ label.y }}mm" class="label {{ label.kind }}">
		<rect
         width="60mm"
         height="65mm"
         rx="5"
         ry="5"
         x="1"
         y="1"
         class="label-border" />
	    <foreignObject
         x="2mm"
         y="2mm"
         width="56mm"
         height="36mm"
         class="header"
         requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility">
			<h1 xmlns="http://www.w3.org/1999/xhtml" class="name">{{ label.name }}</h1>
			<h2 xmlns="http://www.w3.org/1999/xhtml" class="origin">{{ label.origin }}</h2>
			<h3 xmlns="http://www.w3.org/1999/xhtml" class="type">{{ label.type }}</h3>
			<p xmlns="http://www.w3.org/1999/xhtml" class="ingredients">{{ label.ingredients}}</p>
		</foreignObject>
		<image
         xlink:href="{{ label.qr_src }}"
         x="21mm"
         y="40mm"
         width="20mm"
         height="20mm" />
		<text
         x="50mm"
         y="50mm"
         height="5mm"
         width="20mm"
         style="text-align:center;color:white;"
         xml:space="preserve"
         class="temp">{{ label.temp }}</text>
         <rect
         width="10mm"
         height="20mm"
         rx="5"
         ry="5"
         x="45mm"
         y="40mm"
         style="fill:none;stroke:#000000;"
         />

		<text
         x="10mm"
         y="50mm"
         xml:space="preserve"
         class="duration">{{ label.duration }}</text>
         <rect
         width="10mm"
         height="20mm"
         rx="5"
         ry="5"
         x="5mm"
         y="40mm"
         style="fill:none;stroke:#000000;"
         />
	</svg>
    {% endfor %}
</svg>
