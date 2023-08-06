// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.nfrac.comportex.demos.second_level_motor');
goog.require('cljs.core');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.nfrac.comportex.core');
goog.require('cljs.core.async');
goog.require('org.nfrac.comportex.util');
goog.require('org.nfrac.comportex.encoders');
goog.require('clojure.string');
org.nfrac.comportex.demos.second_level_motor.bit_width = (600);
org.nfrac.comportex.demos.second_level_motor.n_on_bits = (30);
org.nfrac.comportex.demos.second_level_motor.motor_bit_width = (10);
org.nfrac.comportex.demos.second_level_motor.motor_n_on_bits = (5);
org.nfrac.comportex.demos.second_level_motor.test_text = "one two three four.\nthe three little pigs.\n6874230\n1874235.\n6342785\n1342780.\n09785341\n29785346.\n04358796\n24358791.";
org.nfrac.comportex.demos.second_level_motor.parse_sentences = (function org$nfrac$comportex$demos$second_level_motor$parse_sentences(text_STAR_){
var text = clojure.string.lower_case(clojure.string.trim(text_STAR_));
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (text){
return (function (p1__73395_SHARP_){
return cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(cljs.core.vec,p1__73395_SHARP_);
});})(text))
,cljs.core.mapv.cljs$core$IFn$_invoke$arity$2(((function (text){
return (function (p1__73394_SHARP_){
return clojure.string.split.cljs$core$IFn$_invoke$arity$2(p1__73394_SHARP_,/[^\w']+/);
});})(text))
,clojure.string.split.cljs$core$IFn$_invoke$arity$2(text,/[^\w]*\.+[^\w]*/)));
});
org.nfrac.comportex.demos.second_level_motor.spec = new cljs.core.PersistentArrayMap(null, 7, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1000)], null),cljs.core.cst$kw$depth,(8),cljs.core.cst$kw$proximal,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$perm_DASH_stable_DASH_inc,0.15,cljs.core.cst$kw$perm_DASH_inc,0.04,cljs.core.cst$kw$perm_DASH_dec,0.01], null),cljs.core.cst$kw$lateral_DASH_synapses_QMARK_,true,cljs.core.cst$kw$distal_DASH_vs_DASH_proximal_DASH_weight,0.0,cljs.core.cst$kw$use_DASH_feedback_QMARK_,true,cljs.core.cst$kw$apical,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$learn_QMARK_,true], null)], null);
org.nfrac.comportex.demos.second_level_motor.higher_level_spec = org.nfrac.comportex.util.deep_merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([org.nfrac.comportex.demos.second_level_motor.spec,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$column_DASH_dimensions,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [(800)], null),cljs.core.cst$kw$stable_DASH_inbit_DASH_frac_DASH_threshold,0.5,cljs.core.cst$kw$ff_DASH_init_DASH_frac,0.05,cljs.core.cst$kw$proximal,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$max_DASH_segments,(5),cljs.core.cst$kw$new_DASH_synapse_DASH_count,(12),cljs.core.cst$kw$learn_DASH_threshold,(6)], null)], null)], 0));
org.nfrac.comportex.demos.second_level_motor.initial_inval = (function org$nfrac$comportex$demos$second_level_motor$initial_inval(sentences){
return new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$sentences,sentences,cljs.core.cst$kw$position,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),(0),(0)], null),cljs.core.cst$kw$value,cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(sentences,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),(0),(0)], null)),cljs.core.cst$kw$action,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$next_DASH_letter_DASH_saccade,(-1),cljs.core.cst$kw$next_DASH_word_DASH_saccade,(-1),cljs.core.cst$kw$next_DASH_sentence_DASH_saccade,(-1)], null)], null);
});
org.nfrac.comportex.demos.second_level_motor.next_position = (function org$nfrac$comportex$demos$second_level_motor$next_position(p__73396,action){
var vec__73398 = p__73396;
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73398,(0),null);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73398,(1),null);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73398,(2),null);
if((cljs.core.cst$kw$next_DASH_sentence_DASH_saccade.cljs$core$IFn$_invoke$arity$1(action) > (0))){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(i + (1)),(0),(0)], null);
} else {
if((cljs.core.cst$kw$next_DASH_sentence_DASH_saccade.cljs$core$IFn$_invoke$arity$1(action) < (0))){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),(0),(0)], null);
} else {
if((cljs.core.cst$kw$next_DASH_word_DASH_saccade.cljs$core$IFn$_invoke$arity$1(action) > (0))){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,(j + (1)),(0)], null);
} else {
if((cljs.core.cst$kw$next_DASH_word_DASH_saccade.cljs$core$IFn$_invoke$arity$1(action) < (0))){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,(0),(0)], null);
} else {
if((cljs.core.cst$kw$next_DASH_letter_DASH_saccade.cljs$core$IFn$_invoke$arity$1(action) > (0))){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,j,(k + (1))], null);
} else {
if((cljs.core.cst$kw$next_DASH_letter_DASH_saccade.cljs$core$IFn$_invoke$arity$1(action) < (0))){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [i,j,(0)], null);
} else {
return null;
}
}
}
}
}
}
});
org.nfrac.comportex.demos.second_level_motor.apply_action = (function org$nfrac$comportex$demos$second_level_motor$apply_action(inval){
var new_posn = org.nfrac.comportex.demos.second_level_motor.next_position(cljs.core.cst$kw$position.cljs$core$IFn$_invoke$arity$1(inval),cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval));
var new_value = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$sentences.cljs$core$IFn$_invoke$arity$1(inval),new_posn);
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(inval,cljs.core.cst$kw$position,new_posn,cljs.core.array_seq([cljs.core.cst$kw$value,new_value], 0));
});
org.nfrac.comportex.demos.second_level_motor.letter_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$value,org.nfrac.comportex.encoders.unique_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.second_level_motor.bit_width], null),org.nfrac.comportex.demos.second_level_motor.n_on_bits)], null);
org.nfrac.comportex.demos.second_level_motor.letter_motor_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$action,cljs.core.cst$kw$next_DASH_letter_DASH_saccade], null),org.nfrac.comportex.encoders.category_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.second_level_motor.motor_bit_width], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1),(-1)], null))], null);
org.nfrac.comportex.demos.second_level_motor.word_motor_sensor = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$action,cljs.core.cst$kw$next_DASH_word_DASH_saccade], null),org.nfrac.comportex.encoders.category_encoder(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.demos.second_level_motor.motor_bit_width], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(1),(-1)], null))], null);
org.nfrac.comportex.demos.second_level_motor.two_region_model = (function org$nfrac$comportex$demos$second_level_motor$two_region_model(var_args){
var args73399 = [];
var len__7211__auto___73402 = arguments.length;
var i__7212__auto___73403 = (0);
while(true){
if((i__7212__auto___73403 < len__7211__auto___73402)){
args73399.push((arguments[i__7212__auto___73403]));

var G__73404 = (i__7212__auto___73403 + (1));
i__7212__auto___73403 = G__73404;
continue;
} else {
}
break;
}

var G__73401 = args73399.length;
switch (G__73401) {
case 0:
return org.nfrac.comportex.demos.second_level_motor.two_region_model.cljs$core$IFn$_invoke$arity$0();

break;
case 1:
return org.nfrac.comportex.demos.second_level_motor.two_region_model.cljs$core$IFn$_invoke$arity$1((arguments[(0)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args73399.length)].join('')));

}
});

org.nfrac.comportex.demos.second_level_motor.two_region_model.cljs$core$IFn$_invoke$arity$0 = (function (){
return org.nfrac.comportex.demos.second_level_motor.two_region_model.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.demos.second_level_motor.spec);
});

org.nfrac.comportex.demos.second_level_motor.two_region_model.cljs$core$IFn$_invoke$arity$1 = (function (spec){
return org.nfrac.comportex.core.region_network(new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$rgn_DASH_0,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input,cljs.core.cst$kw$letter_DASH_motor], null),cljs.core.cst$kw$rgn_DASH_1,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$rgn_DASH_0,cljs.core.cst$kw$word_DASH_motor], null)], null),cljs.core.constantly(org.nfrac.comportex.core.sensory_region),new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$rgn_DASH_0,spec,cljs.core.cst$kw$rgn_DASH_1,org.nfrac.comportex.demos.second_level_motor.higher_level_spec], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$input,org.nfrac.comportex.demos.second_level_motor.letter_sensor], null),new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$letter_DASH_motor,org.nfrac.comportex.demos.second_level_motor.letter_motor_sensor,cljs.core.cst$kw$word_DASH_motor,org.nfrac.comportex.demos.second_level_motor.word_motor_sensor], null));
});

org.nfrac.comportex.demos.second_level_motor.two_region_model.cljs$lang$maxFixedArity = 1;
org.nfrac.comportex.demos.second_level_motor.htm_step_with_action_selection = (function org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection(world_c,control_c){

var c__38109__auto___73480 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___73480){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___73480){
return (function (state_73459){
var state_val_73460 = (state_73459[(1)]);
if((state_val_73460 === (1))){
var state_73459__$1 = state_73459;
var statearr_73461_73481 = state_73459__$1;
(statearr_73461_73481[(2)] = null);

(statearr_73461_73481[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73460 === (2))){
var state_73459__$1 = state_73459;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73459__$1,(4),control_c);
} else {
if((state_val_73460 === (3))){
var inst_73457 = (state_73459[(2)]);
var state_73459__$1 = state_73459;
return cljs.core.async.impl.ioc_helpers.return_chan(state_73459__$1,inst_73457);
} else {
if((state_val_73460 === (4))){
var inst_73445 = (state_73459[(7)]);
var inst_73445__$1 = (state_73459[(2)]);
var state_73459__$1 = (function (){var statearr_73462 = state_73459;
(statearr_73462[(7)] = inst_73445__$1);

return statearr_73462;
})();
if(cljs.core.truth_(inst_73445__$1)){
var statearr_73463_73482 = state_73459__$1;
(statearr_73463_73482[(1)] = (5));

} else {
var statearr_73464_73483 = state_73459__$1;
(statearr_73464_73483[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_73460 === (5))){
var state_73459__$1 = state_73459;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73459__$1,(8),world_c);
} else {
if((state_val_73460 === (6))){
var state_73459__$1 = state_73459;
var statearr_73465_73484 = state_73459__$1;
(statearr_73465_73484[(2)] = null);

(statearr_73465_73484[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73460 === (7))){
var inst_73455 = (state_73459[(2)]);
var state_73459__$1 = state_73459;
var statearr_73466_73485 = state_73459__$1;
(statearr_73466_73485[(2)] = inst_73455);

(statearr_73466_73485[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73460 === (8))){
var inst_73445 = (state_73459[(7)]);
var inst_73448 = (state_73459[(2)]);
var inst_73449 = (inst_73445.cljs$core$IFn$_invoke$arity$1 ? inst_73445.cljs$core$IFn$_invoke$arity$1(inst_73448) : inst_73445.call(null,inst_73448));
var state_73459__$1 = state_73459;
return cljs.core.async.impl.ioc_helpers.put_BANG_(state_73459__$1,(9),world_c,inst_73449);
} else {
if((state_val_73460 === (9))){
var inst_73451 = (state_73459[(2)]);
var state_73459__$1 = (function (){var statearr_73467 = state_73459;
(statearr_73467[(8)] = inst_73451);

return statearr_73467;
})();
var statearr_73468_73486 = state_73459__$1;
(statearr_73468_73486[(2)] = null);

(statearr_73468_73486[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
return null;
}
}
}
}
}
}
}
}
}
});})(c__38109__auto___73480))
;
return ((function (switch__37995__auto__,c__38109__auto___73480){
return (function() {
var org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto__ = null;
var org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto____0 = (function (){
var statearr_73472 = [null,null,null,null,null,null,null,null,null];
(statearr_73472[(0)] = org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto__);

(statearr_73472[(1)] = (1));

return statearr_73472;
});
var org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto____1 = (function (state_73459){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_73459);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e73473){if((e73473 instanceof Object)){
var ex__37999__auto__ = e73473;
var statearr_73474_73487 = state_73459;
(statearr_73474_73487[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_73459);

return cljs.core.cst$kw$recur;
} else {
throw e73473;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__73488 = state_73459;
state_73459 = G__73488;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto__ = function(state_73459){
switch(arguments.length){
case 0:
return org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto____0.call(this);
case 1:
return org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto____1.call(this,state_73459);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto____0;
org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto____1;
return org$nfrac$comportex$demos$second_level_motor$htm_step_with_action_selection_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___73480))
})();
var state__38111__auto__ = (function (){var statearr_73475 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_73475[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___73480);

return statearr_73475;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___73480))
);


return (function (htm,inval){
var htm_a = org.nfrac.comportex.protocols.htm_learn(org.nfrac.comportex.protocols.htm_activate(org.nfrac.comportex.protocols.htm_sense(htm,inval,cljs.core.cst$kw$sensory)));
var vec__73476 = cljs.core.cst$kw$position.cljs$core$IFn$_invoke$arity$1(inval);
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73476,(0),null);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73476,(1),null);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73476,(2),null);
var sentences = cljs.core.cst$kw$sentences.cljs$core$IFn$_invoke$arity$1(inval);
var sentence = cljs.core.get.cljs$core$IFn$_invoke$arity$2(sentences,i);
var word = cljs.core.get.cljs$core$IFn$_invoke$arity$2(sentence,j);
var end_of_word_QMARK_ = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(k,(cljs.core.count(word) - (1)));
var end_of_sentence_QMARK_ = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(j,(cljs.core.count(sentence) - (1)));
var end_of_passage_QMARK_ = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(i,(cljs.core.count(sentences) - (1)));
var r0_lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm_a,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$rgn_DASH_0,cljs.core.cst$kw$layer_DASH_3], null));
var r1_lyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm_a,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$rgn_DASH_1,cljs.core.cst$kw$layer_DASH_3], null));
var r0_stability = (cljs.core.count(cljs.core.cst$kw$out_DASH_stable_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(r0_lyr))) / cljs.core.count(cljs.core.cst$kw$out_DASH_ff_DASH_bits.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$state.cljs$core$IFn$_invoke$arity$1(r0_lyr))));
var word_burst_QMARK_ = (function (){var G__73477 = cljs.core.cst$kw$word_DASH_bursting_QMARK_.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval));
if((k > (0))){
var or__6153__auto__ = G__73477;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return (r0_stability < 0.5);
}
} else {
return G__73477;
}
})();
var sent_burst_QMARK_ = (function (){var G__73478 = cljs.core.cst$kw$sentence_DASH_bursting_QMARK_.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval));
if((k > (0))){
var or__6153__auto__ = G__73478;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return (r0_stability < 0.5);
}
} else {
return G__73478;
}
})();
var action_STAR_ = ((!(end_of_word_QMARK_))?new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$next_DASH_letter_DASH_saccade,(1)], null):(cljs.core.truth_(word_burst_QMARK_)?new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$next_DASH_letter_DASH_saccade,(-1),cljs.core.cst$kw$word_DASH_bursting_QMARK_,false], null):((!(end_of_sentence_QMARK_))?new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$next_DASH_word_DASH_saccade,(1),cljs.core.cst$kw$next_DASH_letter_DASH_saccade,(-1),cljs.core.cst$kw$word_DASH_bursting_QMARK_,false], null):(cljs.core.truth_(sent_burst_QMARK_)?new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$next_DASH_word_DASH_saccade,(-1),cljs.core.cst$kw$next_DASH_letter_DASH_saccade,(-1),cljs.core.cst$kw$word_DASH_bursting_QMARK_,false,cljs.core.cst$kw$sentence_DASH_bursting_QMARK_,false], null):((!(end_of_passage_QMARK_))?new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$next_DASH_sentence_DASH_saccade,(1),cljs.core.cst$kw$next_DASH_word_DASH_saccade,(1),cljs.core.cst$kw$next_DASH_letter_DASH_saccade,(-1),cljs.core.cst$kw$word_DASH_bursting_QMARK_,false,cljs.core.cst$kw$sentence_DASH_bursting_QMARK_,false], null):new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$next_DASH_word_DASH_saccade,(-1),cljs.core.cst$kw$next_DASH_letter_DASH_saccade,(-1),cljs.core.cst$kw$word_DASH_bursting_QMARK_,false,cljs.core.cst$kw$sentence_DASH_bursting_QMARK_,false], null)
)))));
var action = cljs.core.merge.cljs$core$IFn$_invoke$arity$variadic(cljs.core.array_seq([new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$next_DASH_word_DASH_saccade,(0),cljs.core.cst$kw$next_DASH_sentence_DASH_saccade,(0),cljs.core.cst$kw$word_DASH_bursting_QMARK_,word_burst_QMARK_,cljs.core.cst$kw$sentence_DASH_bursting_QMARK_,sent_burst_QMARK_], null),action_STAR_], 0));
var inval_with_action = cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(inval,cljs.core.cst$kw$action,action,cljs.core.array_seq([cljs.core.cst$kw$prev_DASH_action,cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval)], 0));
var new_inval_73489 = org.nfrac.comportex.demos.second_level_motor.apply_action(inval_with_action);
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(world_c,new_inval_73489);

var G__73479 = htm_a;
var G__73479__$1 = org.nfrac.comportex.protocols.htm_sense(G__73479,inval_with_action,cljs.core.cst$kw$motor)
;
var G__73479__$2 = org.nfrac.comportex.protocols.htm_depolarise(G__73479__$1)
;
var G__73479__$3 = ((end_of_word_QMARK_)?cljs.core.update_in.cljs$core$IFn$_invoke$arity$4(G__73479__$2,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$rgn_DASH_0], null),org.nfrac.comportex.protocols.break$,cljs.core.cst$kw$tm):G__73479__$2);
var G__73479__$4 = (((end_of_word_QMARK_) && (cljs.core.not(word_burst_QMARK_)))?cljs.core.update_in.cljs$core$IFn$_invoke$arity$4(G__73479__$3,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$rgn_DASH_0], null),org.nfrac.comportex.protocols.break$,cljs.core.cst$kw$syns):G__73479__$3);
if((end_of_word_QMARK_) && (cljs.core.not(word_burst_QMARK_))){
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$4(G__73479__$4,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$rgn_DASH_1], null),org.nfrac.comportex.protocols.break$,cljs.core.cst$kw$winners);
} else {
return G__73479__$4;
}
});
});
