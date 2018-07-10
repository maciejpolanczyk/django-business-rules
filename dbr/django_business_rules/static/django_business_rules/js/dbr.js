var actions_conditions, form, submit, rule_set;
(function($) {

  function onReady() {

    actions_conditions = [];

    rules = JSON.parse($('#rules').val());
    rule_set = $('.rule_set');
    ruleData = JSON.parse($('#rule_data').val());
    form = $('#br_form');

    if (rules.length == 0 || typeof(rules.length) == 'undefined') {
        appendEmptyRule();
    } else {
      $.each(rules, function(index, one_rule){
        rule_set.append(getRule());
        addActionsConditions(index);
      });

      initializeActionsConditions(ruleData, rules);
    }
    initializeForm();
  }

  function addActionsConditions(index) {
    var rule_object = {
        conditions: rule_set.find('.one_rule:eq(' + index + ')').find('.conditions').first(),
        actions: rule_set.find('.one_rule:eq(' + index + ')').find('.actions').first()
    }
    actions_conditions.splice(index, 0, rule_object);
  }

  function initializeActionsConditions(ruleData, rules) {
    data = ruleData;
    $.each(rules, function(index, one_rule){
      data['data'] = one_rule.conditions;
      actions_conditions[index]['conditions'].conditionsBuilder(data)
      data['data'] = one_rule.actions;
      actions_conditions[index]['actions'].actionsBuilder(data)
    });
  }

  function getRule() {
    // TODO use the django language processor for phrases
    var one_rule = $("<div>", {"class": "one_rule"});
    one_rule.append($('<h2>When these conditions are met...</h2>'));
    one_rule.append($("<div>", {"class": "conditions"}));
    one_rule.append($('<h2>Do these actions...</h2>'));
    one_rule.append($("<div>", {"class": "actions"}));

    var insertRuleLink = $("<a>", {"href": "#", "text": "Insert Rule Below"});
    insertRuleLink.click(function(e) {
      e.preventDefault();
      insertEmptyRuleAfter(one_rule);
    });
    one_rule.append(insertRuleLink);

    var moveUpLink = $("<a>", {"class": "remove", "href": "#", "text": "Move Rule Up"});
    moveUpLink.click(function(e) {
      e.preventDefault();
      moveRuleUp(one_rule);
    });
    one_rule.append(moveUpLink);

    var removeLink = $("<a>", {"class": "remove", "href": "#", "text": "Remove Preceding Rule"});
    removeLink.click(function(e) {
      e.preventDefault();
      var index = rule_set.find('.one_rule').index(one_rule);
      actions_conditions.splice(index, 1);
      one_rule.remove();
    });
    one_rule.append(removeLink);

    return one_rule;
  }

  function appendEmptyRule() {
    var index = rule_set.find('.one_rule').length || 0;
    rule_set.append(getRule());
    initializeEmptyRule(index);
  }

  function insertEmptyRuleAfter(a_rule) {
    var index = rule_set.find('.one_rule').index(a_rule);
    getRule().insertAfter(a_rule);
    initializeEmptyRule(index + 1);
  }

  function initializeEmptyRule(index) {
    addActionsConditions(index)
    var data = ruleData;
    data['data'] = null;
    actions_conditions[index]['conditions'].conditionsBuilder(data);
    actions_conditions[index]['actions'].actionsBuilder(data);
  }

  function moveRuleUp(a_rule) {
    var index = rule_set.find('.one_rule').index(a_rule);
    if (index == 0) {
      return;
    }
    a_rule.insertBefore(a_rule.prev());
    var tmp = actions_conditions[index];
    actions_conditions[index] = actions_conditions[index - 1];
    actions_conditions[index - 1] = tmp;
  }

  function initializeForm() {
    form.submit(function(e) {
      var rule_set = $('.rule_set').find('.one_rule');
      var rules = []
      rule_set.each(function(index, one_rule){
        rules[index] = {
          'conditions': actions_conditions[index]['conditions'].conditionsBuilder('data'),
          'actions': actions_conditions[index]['actions'].actionsBuilder('data')
        }
      });
      $('#rules').val(JSON.stringify(rules));
      return true;
    });
  }
  $(onReady);
})(jQuery);
