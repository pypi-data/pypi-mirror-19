# -*- coding: utf-8 -*-

js_function = """function addSummary(topsuite)
{
    var opts = {logURL: window.settings.logURL};
    $.tmpl('summaryTableTemplate', topsuite, opts).insertAfter($('#header'));
	
	var canvas = document.getElementById("can");
	var ctx = canvas.getContext("2d");
	var lastend = 0;
	var data = [topsuite.totalFailed , topsuite.totalPassed];
	var data_total = 0;
	var color1 = ['red','green'];
	var color2 = ['darkred','lightgreen'];

	for(var e = 0; e < data.length; e++)
	{
		data_total += data[e];
	}

	for (var i = 0; i < data.length; i++) 
	{
		var gradient = ctx.createLinearGradient(0, 0, 0, 170);
		gradient.addColorStop(0, color1[i]);
		gradient.addColorStop(1, color2[i]);

		ctx.fillStyle = gradient;
		ctx.beginPath();
		ctx.moveTo(canvas.width/2,canvas.height/2);
		ctx.arc(canvas.width/2,canvas.height/2,canvas.height/2,lastend,lastend+(Math.PI*2*(data[i]/data_total)),false);
		ctx.lineTo(canvas.width/2,canvas.height/2);
		ctx.fill();
		lastend += Math.PI*2*(data[i]/data_total);
	}
}"""

html_template = """<script type="text/x-jquery-tmpl" id="summaryTableTemplate">
  <h2>Summary Information</h2>
  <table class="details">
    <tr>
      <th>Status:</th>
      {{if criticalFailed}}
      <td><a href="#totals?critical" onclick="totalDetailSelected('critical')"
             class="fail">${criticalFailed} critical test{{if criticalFailed != 1}}s{{/if}} failed</a></td>
      {{else totalFailed}}
      <td><a href="#totals?critical" onclick="totalDetailSelected('critical')"
             class="pass">All critical tests passed</a></td>
      {{else}}
      <td><a href="#totals?all" onclick="totalDetailSelected('all')"
             class="pass">All tests passed</a></td>
      {{/if}}
    </tr>
    {{if doc()}}
    <tr>
      <th>Documentation:</th>
      <td class="doc">{{html doc()}}</td>
    </tr>
    {{/if}}
    {{each metadata}}
    <tr>
      <th>{{html $value[0]}}:</th>
      <td class="doc">{{html $value[1]}}</td>
    </tr>
    {{/each}}
    {{if times.startTime != 'N/A'}}
    <tr>
      <th>Start Time:</th>
      <td>${times.startTime}</td>
    </tr>
    {{/if}}
    {{if times.endTime != 'N/A'}}
    <tr>
      <th>End Time:</th>
      <td>${times.endTime}</td>
    </tr>
    {{/if}}
    <tr>
      <th>Elapsed Time:</th>
      <td>${times.elapsedTime}</td>
    </tr>
    {{if $item.logURL}}
    <tr>
      <th>Log File:</th>
      <td><a href="${$item.logURL}">${$item.logURL}</a></td>
    </tr>
    {{/if}}
	
	<tr>
	
		<td>
		
			<br /><canvas id="can" width="250" height="250" style="margin: auto;" /></canvas><br /><br />

			<table style="background-color: #FFFFFF; text-align: center;">
			<tr>
			<td style="background-color: #b30000; width: 15px; height: 15px; border-radius: 5px;"> </td>
			<td style="width: 80px;">FAIL</td>
			<td style="background-color: #009900; width: 15px; height: 15px; border-radius: 5px;"> </td>
			<td style="width: 80px;">PASS</td>
			</tr>
			</table>
		
		</td>
	
	</tr>
	
  </table>
  
</script>"""