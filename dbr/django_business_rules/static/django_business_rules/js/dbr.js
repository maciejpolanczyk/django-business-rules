var conditions, actions, submit, allData;
(function($) {

  function onReady() {
    conditions = $('#conditions');
    actions = $('#actions');
    form = $('#br_form');
    rules = JSON.parse($('#rules').val());
    ruleData = JSON.parse($('#rule_data').val());

    initializeConditions(ruleData, rules);
    initializeActions(ruleData, rules);
    initializeForm();
  }

  function initializeConditions(ruleData, rules) {
    data = ruleData;
    if (rules.length > 0) {
        data['data'] = rules[0].conditions;
    }
    conditions.conditionsBuilder(data)
  }

  function initializeActions(ruleData, rules) {
    data = ruleData;
    if (rules.length > 0) {
        data['data'] = rules[0].actions;
    }
    actions.actionsBuilder(data);
  }

  function initializeForm() {

    form.submit(function(e) {
      rules = [{
        'conditions': conditions.conditionsBuilder('data'),
        'actions': actions.actionsBuilder('data')
      }];
      $('#rules').val(JSON.stringify(rules));
      return true;
    });
  }
  $(onReady);
})(jQuery);
