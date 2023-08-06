## -*- coding: utf-8 -*-
<%inherit file="/shifts/base.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  ${self.edit_timetable_javascript()}
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  ${self.edit_timetable_styles()}
</%def>

<%def name="context_menu()">
  % if request.has_perm('timesheet.view'):
      <li>${h.link_to("View this Time Sheet", url('timesheet.employee'))}</li>
  % endif
  % if request.has_perm('schedule.view'):
      <li>${h.link_to("View this Schedule", url('schedule.employee'))}</li>
  % endif
</%def>

<%def name="render_day(day)">
  % for shift in day['worked_shifts']:
      <p class="shift" data-uuid="${shift.uuid}">
        ${render_shift(shift)}
      </p>
  % endfor
</%def>

<%def name="render_employee_total(employee)">
  ${employee.worked_hours_display}
</%def>

<%def name="edit_form()">
  ${h.form(url('timesheet.employee.edit'), id='timetable-form')}
  ${h.csrf_token(request)}
</%def>

<%def name="edit_tools()">
  <div class="buttons">
    <button type="button" class="save-changes" disabled="disabled">Save Changes</button>
    <button type="button" class="undo-changes" disabled="disabled">Undo Changes</button>
  </div>
</%def>


${self.timesheet_wrapper(with_edit_form=True, change_employee='confirm_leave')}

${edit_tools()}

<div id="day-editor" style="display: none;">
  <div class="shifts"></div>
  <button type="button" id="add-shift">Add Shift</button>
</div>

<div id="snippets">
  <div class="shift" data-uuid="">
    ${h.text('edit_start_time')} thru ${h.text('edit_end_time')}
    <button type="button"><span class="ui-icon ui-icon-trash"></span></button>
  </div>
</div>
