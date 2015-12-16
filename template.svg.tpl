<svg  xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
	  width="210mm" height="{{ doc_height }}mm"
	  version="1.2"
	  >
	<style type="text/css">
		<![CDATA[
		rect.label{fill:none;stroke:#000000;stroke-opacity:1}
		rect.label.black{stroke:dimgrey;}
		rect.label.red{stroke:maroon;}
		rect.label.infusion{stroke:LightSeaGreen;}
		rect.label.green{stroke:ForestGreen;}
		rect.label.smoked{stroke:peru;}
		text{}
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
         style="font-size:16px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans">{{ label.name }}</text>
      <text
         x="30mm"
         y="32px"
         xml:space="preserve"
         style="font-size:14px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans">{{ label.origin }}</text>
      <text
         x="10mm"
         y="56px"
		 width="20mm"
         xml:space="preserve"
         style="font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans">{{ label.type }}</text>
      <text
         x="30mm"
         y="56px"
         xml:space="preserve"
         style="font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans">duration</text>
      <text
         x="50mm"
         y="56px"
         xml:space="preserve"
         style="font-size:12px;font-style:normal;font-weight:normal;text-align:center;line-height:125%;letter-spacing:0px;word-spacing:0px;text-anchor:middle;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans">temp</text>
      <image
         xlink:href="{{ label.qr_src }}"
         x="21mm"
         y="40mm"
         width="20mm"
         height="20mm" />
      <text
         x="2mm"
         y="75px"
		 width="50mm"
         id="text3942"
         xml:space="preserve"
         style="font-size:11px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans">* ingredient 1</text>
    </svg>
    {% endfor %}
</svg>
