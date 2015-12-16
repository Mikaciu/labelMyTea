<svg  xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
	  width="210mm" height="{{ doc_height }}mm" viewBox="0 0 210mm {{ doc_height }}mm" streamable="true"
	  version="1.2"
	  >
	<style type="text/css">
		<![CDATA[
		
		rect.label{fill:none;stroke:navy;stroke-opacity:1;stroke-width:0.5mm;}
		rect.label.black{stroke:dimgrey;}
		rect.label.red{stroke:maroon;}
		rect.label.infusion{stroke:LightSeaGreen;}
		rect.label.green{stroke:ForestGreen;}
		rect.label.smoked{stroke:peru;}
		text.title{font-size:16px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.origin{font-size:14px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.type{font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.duration{font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		text.temp{text-anchor:middle;font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans;width:10mm;color:white;}
		foreignObject.ingredients{font-size:11px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans}
		foreignObject.ingredients p{text-align:center;}
		]]>
	</style>
	{% for label in labels %}
	<svg x="{{ label.x }}mm" y="{{ label.y }}mm">
		<rect
         width="60mm"
         height="65mm"
         rx="5"
         ry="5"
         x="1"
         y="1"
         style="" class="label {{ label.kind }}" />
		<text
         x="30mm"
         y="16px"
         xml:space="preserve"
         class="title">{{ label.name }}</text>
		<text
         x="30mm"
         y="40px"
         xml:space="preserve"
         class="origin">{{ label.origin }}</text>
		<text
         x="30mm"
         y="64px"
         xml:space="preserve"
         class="type">{{ label.type }}</text>
		<foreignObject
         x="2mm"
         y="65px"
         width="56mm"
         height="20mm"
         class="ingredients"
         requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility">
			<p xmlns="http://www.w3.org/1999/xhtml">{{ label.ingredients}}</p>
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
