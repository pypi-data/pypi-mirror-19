# -*- coding: utf-8 -*-

js_function = """function addSummary(topsuite) {
    var opts = {logURL: window.settings.logURL};
    $.tmpl('summaryTableTemplate', topsuite, opts).insertAfter($('#header'));
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
  </table>
</script>"""