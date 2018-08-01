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
        name: rule_set.find('.one_rule:eq(' + index + ')').find('.rule_name').first(),
        conditions: rule_set.find('.one_rule:eq(' + index + ')').find('.conditions').first(),
        actions: rule_set.find('.one_rule:eq(' + index + ')').find('.actions').first()
    }
    actions_conditions.splice(index, 0, rule_object);
  }

  function initializeActionsConditions(ruleData, rules) {
    data = ruleData;
    $.each(rules, function(index, one_rule){
      actions_conditions[index]['name'].val(one_rule.name);
      data['data'] = one_rule.conditions;
      actions_conditions[index]['conditions'].conditionsBuilder(data)
      data['data'] = one_rule.actions;
      actions_conditions[index]['actions'].actionsBuilder(data)
    });
  }

  function getRule() {
    // TODO use the django language processor for phrases
    var one_rule = $("<div>", {"class": "one_rule"});

    var rule_name_label = $("<label>", {"text": "Name:"});
    var rule_name = $("<input>", {"class": "rule_name", "type": "text"});
    rule_name_label.append(rule_name);
    one_rule.append(rule_name_label);

    var toggleDetail = $("<a>", {"class": "rule_control", "href": "#", "text": "Toggle Detail"});
    toggleDetail.click(function(e) {
      e.preventDefault();
      one_rule.find('.rule_detail').toggleClass('hidden');
    });
    one_rule.append(toggleDetail);

    var insertRuleLink = $("<a>", {"class": "rule_control", "href": "#", "text": "Insert Rule Below"});
    insertRuleLink.click(function(e) {
      e.preventDefault();
      insertEmptyRuleAfter(one_rule);
    });
    one_rule.append(insertRuleLink);

    var moveUpLink = $("<a>", {"class": "rule_control", "href": "#", "text": "Move Rule Up"});
    moveUpLink.click(function(e) {
      e.preventDefault();
      moveRuleUp(one_rule);
    });
    one_rule.append(moveUpLink);

    var removeLink = $("<a>", {"class": "rule_control remove", "href": "#", "text": "Remove Rule"});
    removeLink.click(function(e) {
      e.preventDefault();
      var index = rule_set.find('.one_rule').index(one_rule);
      actions_conditions.splice(index, 1);
      one_rule.remove();
    });
    one_rule.append(removeLink);

    var rule_detail = $("<div>", {"class": "rule_detail hidden"});
    rule_detail.append($('<h2>When these conditions are met...</h2>'));
    rule_detail.append($("<div>", {"class": "conditions"}));
    rule_detail.append($('<h2>Do these actions...</h2>'));
    rule_detail.append($("<div>", {"class": "actions"}));
    one_rule.append(rule_detail);

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
          'name': $(actions_conditions[index]['name']).val(),
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
