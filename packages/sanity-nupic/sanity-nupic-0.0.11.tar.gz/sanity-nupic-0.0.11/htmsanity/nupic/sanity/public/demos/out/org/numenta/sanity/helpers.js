// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.helpers');
goog.require('cljs.core');
goog.require('goog.dom');
goog.require('goog.dom.classes');
goog.require('reagent.core');
goog.require('org.nfrac.comportex.protocols');
goog.require('org.numenta.sanity.util');
goog.require('cljs.core.async');
goog.require('org.nfrac.comportex.core');
goog.require('goog.events');
goog.require('org.nfrac.comportex.util');
goog.require('goog.style');
org.numenta.sanity.helpers.loading_message_element = (function org$numenta$sanity$helpers$loading_message_element(){
return goog.dom.getElement("loading-message");
});
org.numenta.sanity.helpers.show = (function org$numenta$sanity$helpers$show(el){
return goog.dom.classes.add(el,"show");
});
org.numenta.sanity.helpers.hide = (function org$numenta$sanity$helpers$hide(el){
return goog.dom.classes.remove(el,"show");
});
org.numenta.sanity.helpers.ui_loading_message_until = (function org$numenta$sanity$helpers$ui_loading_message_until(finished_c){
var el = org.numenta.sanity.helpers.loading_message_element();
org.numenta.sanity.helpers.show(el);

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,el){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,el){
return (function (state_46242){
var state_val_46243 = (state_46242[(1)]);
if((state_val_46243 === (1))){
var state_46242__$1 = state_46242;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_46242__$1,(2),finished_c);
} else {
if((state_val_46243 === (2))){
var inst_46239 = (state_46242[(2)]);
var inst_46240 = org.numenta.sanity.helpers.hide(el);
var state_46242__$1 = (function (){var statearr_46244 = state_46242;
(statearr_46244[(7)] = inst_46240);

return statearr_46244;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_46242__$1,inst_46239);
} else {
return null;
}
}
});})(c__38109__auto__,el))
;
return ((function (switch__37995__auto__,c__38109__auto__,el){
return (function() {
var org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto____0 = (function (){
var statearr_46248 = [null,null,null,null,null,null,null,null];
(statearr_46248[(0)] = org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto__);

(statearr_46248[(1)] = (1));

return statearr_46248;
});
var org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto____1 = (function (state_46242){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_46242);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e46249){if((e46249 instanceof Object)){
var ex__37999__auto__ = e46249;
var statearr_46250_46252 = state_46242;
(statearr_46250_46252[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_46242);

return cljs.core.cst$kw$recur;
} else {
throw e46249;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__46253 = state_46242;
state_46242 = G__46253;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto__ = function(state_46242){
switch(arguments.length){
case 0:
return org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto____1.call(this,state_46242);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto____0;
org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto____1;
return org$numenta$sanity$helpers$ui_loading_message_until_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,el))
})();
var state__38111__auto__ = (function (){var statearr_46251 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_46251[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_46251;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,el))
);

return c__38109__auto__;
});
org.numenta.sanity.helpers.with_ui_loading_message = (function org$numenta$sanity$helpers$with_ui_loading_message(f){
return org.numenta.sanity.helpers.ui_loading_message_until((function (){var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__){
return (function (state_46274){
var state_val_46275 = (state_46274[(1)]);
if((state_val_46275 === (1))){
var inst_46269 = cljs.core.async.timeout((100));
var state_46274__$1 = state_46274;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_46274__$1,(2),inst_46269);
} else {
if((state_val_46275 === (2))){
var inst_46271 = (state_46274[(2)]);
var inst_46272 = (f.cljs$core$IFn$_invoke$arity$0 ? f.cljs$core$IFn$_invoke$arity$0() : f.call(null));
var state_46274__$1 = (function (){var statearr_46276 = state_46274;
(statearr_46276[(7)] = inst_46271);

return statearr_46276;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_46274__$1,inst_46272);
} else {
return null;
}
}
});})(c__38109__auto__))
;
return ((function (switch__37995__auto__,c__38109__auto__){
return (function() {
var org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto____0 = (function (){
var statearr_46280 = [null,null,null,null,null,null,null,null];
(statearr_46280[(0)] = org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto__);

(statearr_46280[(1)] = (1));

return statearr_46280;
});
var org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto____1 = (function (state_46274){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_46274);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e46281){if((e46281 instanceof Object)){
var ex__37999__auto__ = e46281;
var statearr_46282_46284 = state_46274;
(statearr_46282_46284[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_46274);

return cljs.core.cst$kw$recur;
} else {
throw e46281;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__46285 = state_46274;
state_46274 = G__46285;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto__ = function(state_46274){
switch(arguments.length){
case 0:
return org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto____1.call(this,state_46274);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto____0;
org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto____1;
return org$numenta$sanity$helpers$with_ui_loading_message_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__))
})();
var state__38111__auto__ = (function (){var statearr_46283 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_46283[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_46283;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__))
);

return c__38109__auto__;
})());
});
org.numenta.sanity.helpers.text_world_input_component = (function org$numenta$sanity$helpers$text_world_input_component(inval,htm,max_shown,scroll_every,separator){
var time = org.nfrac.comportex.protocols.timestep(htm);
var show_n = (max_shown - cljs.core.mod((max_shown - time),scroll_every));
var history = cljs.core.take_last(show_n,cljs.core.cst$kw$history.cljs$core$IFn$_invoke$arity$1(cljs.core.meta(inval)));
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,(function (){var iter__6925__auto__ = ((function (time,show_n,history){
return (function org$numenta$sanity$helpers$text_world_input_component_$_iter__46296(s__46297){
return (new cljs.core.LazySeq(null,((function (time,show_n,history){
return (function (){
var s__46297__$1 = s__46297;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46297__$1);
if(temp__4657__auto__){
var s__46297__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__46297__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46297__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46299 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46298 = (0);
while(true){
if((i__46298 < size__6924__auto__)){
var vec__46304 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46298);
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46304,(0),null);
var word = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46304,(1),null);
var t = (i + (time - (cljs.core.count(history) - (1))));
var curr_QMARK_ = (time === t);
cljs.core.chunk_append(b__46299,cljs.core.with_meta(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [((curr_QMARK_)?cljs.core.cst$kw$ins:cljs.core.cst$kw$span),[cljs.core.str(word),cljs.core.str(separator)].join('')], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,[cljs.core.str(word),cljs.core.str(t)].join('')], null)));

var G__46306 = (i__46298 + (1));
i__46298 = G__46306;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46299),org$numenta$sanity$helpers$text_world_input_component_$_iter__46296(cljs.core.chunk_rest(s__46297__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46299),null);
}
} else {
var vec__46305 = cljs.core.first(s__46297__$2);
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46305,(0),null);
var word = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46305,(1),null);
var t = (i + (time - (cljs.core.count(history) - (1))));
var curr_QMARK_ = (time === t);
return cljs.core.cons(cljs.core.with_meta(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [((curr_QMARK_)?cljs.core.cst$kw$ins:cljs.core.cst$kw$span),[cljs.core.str(word),cljs.core.str(separator)].join('')], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,[cljs.core.str(word),cljs.core.str(t)].join('')], null)),org$numenta$sanity$helpers$text_world_input_component_$_iter__46296(cljs.core.rest(s__46297__$2)));
}
} else {
return null;
}
break;
}
});})(time,show_n,history))
,null,null));
});})(time,show_n,history))
;
return iter__6925__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,history));
})()], null);
});
org.numenta.sanity.helpers.predictions_table = (function org$numenta$sanity$helpers$predictions_table(predictions){
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$table$table,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tbody,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"prediction"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"votes %"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"votes per bit"], null)], null),(function (){var iter__6925__auto__ = (function org$numenta$sanity$helpers$predictions_table_$_iter__46325(s__46326){
return (new cljs.core.LazySeq(null,(function (){
var s__46326__$1 = s__46326;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__46326__$1);
if(temp__4657__auto__){
var s__46326__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__46326__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__46326__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__46328 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__46327 = (0);
while(true){
if((i__46327 < size__6924__auto__)){
var vec__46337 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__46327);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46337,(0),null);
var map__46338 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46337,(1),null);
var map__46338__$1 = ((((!((map__46338 == null)))?((((map__46338.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46338.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46338):map__46338);
var value = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46338__$1,cljs.core.cst$kw$value);
var votes_frac = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46338__$1,cljs.core.cst$kw$votes_DASH_frac);
var votes_per_bit = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46338__$1,cljs.core.cst$kw$votes_DASH_per_DASH_bit);
cljs.core.chunk_append(b__46328,(function (){var txt = value;
return cljs.core.with_meta(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,txt], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td$text_DASH_right,[cljs.core.str(org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((votes_frac * (100))))].join('')], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td$text_DASH_right,[cljs.core.str(org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1(votes_per_bit))].join('')], null)], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,[cljs.core.str(txt),cljs.core.str(j)].join('')], null));
})());

var G__46343 = (i__46327 + (1));
i__46327 = G__46343;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__46328),org$numenta$sanity$helpers$predictions_table_$_iter__46325(cljs.core.chunk_rest(s__46326__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__46328),null);
}
} else {
var vec__46340 = cljs.core.first(s__46326__$2);
var j = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46340,(0),null);
var map__46341 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46340,(1),null);
var map__46341__$1 = ((((!((map__46341 == null)))?((((map__46341.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46341.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46341):map__46341);
var value = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46341__$1,cljs.core.cst$kw$value);
var votes_frac = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46341__$1,cljs.core.cst$kw$votes_DASH_frac);
var votes_per_bit = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46341__$1,cljs.core.cst$kw$votes_DASH_per_DASH_bit);
return cljs.core.cons((function (){var txt = value;
return cljs.core.with_meta(new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,txt], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td$text_DASH_right,[cljs.core.str(org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((votes_frac * (100))))].join('')], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td$text_DASH_right,[cljs.core.str(org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1(votes_per_bit))].join('')], null)], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,[cljs.core.str(txt),cljs.core.str(j)].join('')], null));
})(),org$numenta$sanity$helpers$predictions_table_$_iter__46325(cljs.core.rest(s__46326__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,predictions));
})()], null)], null)], null);
});
org.numenta.sanity.helpers.text_world_predictions_component = (function org$numenta$sanity$helpers$text_world_predictions_component(htm,n_predictions){
var vec__46345 = cljs.core.first(cljs.core.vals(cljs.core.cst$kw$sensors.cljs$core$IFn$_invoke$arity$1(htm)));
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46345,(0),null);
var e = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46345,(1),null);
var rgn = cljs.core.first(org.nfrac.comportex.core.region_seq(htm));
var pr_votes = org.nfrac.comportex.core.predicted_bit_votes(rgn);
var predictions = org.nfrac.comportex.protocols.decode(e,pr_votes,n_predictions);
return org.numenta.sanity.helpers.predictions_table(predictions);
});
org.numenta.sanity.helpers.canvas$call_draw_fn = (function org$numenta$sanity$helpers$canvas$call_draw_fn(component){
var vec__46348 = reagent.core.argv(component);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46348,(0),null);
var ___$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46348,(1),null);
var ___$2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46348,(2),null);
var ___$3 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46348,(3),null);
var ___$4 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46348,(4),null);
var draw = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46348,(5),null);
var G__46349 = reagent.core.dom_node(component).getContext("2d");
return (draw.cljs$core$IFn$_invoke$arity$1 ? draw.cljs$core$IFn$_invoke$arity$1(G__46349) : draw.call(null,G__46349));
});
org.numenta.sanity.helpers.canvas = (function org$numenta$sanity$helpers$canvas(_,___$1,___$2,___$3,___$4){
return reagent.core.create_class(new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$component_DASH_did_DASH_mount,(function (p1__46350_SHARP_){
return org.numenta.sanity.helpers.canvas$call_draw_fn(p1__46350_SHARP_);
}),cljs.core.cst$kw$component_DASH_did_DASH_update,(function (p1__46351_SHARP_){
return org.numenta.sanity.helpers.canvas$call_draw_fn(p1__46351_SHARP_);
}),cljs.core.cst$kw$display_DASH_name,"canvas",cljs.core.cst$kw$reagent_DASH_render,(function (props,width,height,canaries,___$5){
var seq__46358_46364 = cljs.core.seq(canaries);
var chunk__46359_46365 = null;
var count__46360_46366 = (0);
var i__46361_46367 = (0);
while(true){
if((i__46361_46367 < count__46360_46366)){
var v_46368 = chunk__46359_46365.cljs$core$IIndexed$_nth$arity$2(null,i__46361_46367);
if(((!((v_46368 == null)))?((((v_46368.cljs$lang$protocol_mask$partition0$ & (32768))) || (v_46368.cljs$core$IDeref$))?true:(((!v_46368.cljs$lang$protocol_mask$partition0$))?cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46368):false)):cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46368))){
(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(v_46368) : cljs.core.deref.call(null,v_46368));
} else {
}

var G__46369 = seq__46358_46364;
var G__46370 = chunk__46359_46365;
var G__46371 = count__46360_46366;
var G__46372 = (i__46361_46367 + (1));
seq__46358_46364 = G__46369;
chunk__46359_46365 = G__46370;
count__46360_46366 = G__46371;
i__46361_46367 = G__46372;
continue;
} else {
var temp__4657__auto___46373 = cljs.core.seq(seq__46358_46364);
if(temp__4657__auto___46373){
var seq__46358_46374__$1 = temp__4657__auto___46373;
if(cljs.core.chunked_seq_QMARK_(seq__46358_46374__$1)){
var c__6956__auto___46375 = cljs.core.chunk_first(seq__46358_46374__$1);
var G__46376 = cljs.core.chunk_rest(seq__46358_46374__$1);
var G__46377 = c__6956__auto___46375;
var G__46378 = cljs.core.count(c__6956__auto___46375);
var G__46379 = (0);
seq__46358_46364 = G__46376;
chunk__46359_46365 = G__46377;
count__46360_46366 = G__46378;
i__46361_46367 = G__46379;
continue;
} else {
var v_46380 = cljs.core.first(seq__46358_46374__$1);
if(((!((v_46380 == null)))?((((v_46380.cljs$lang$protocol_mask$partition0$ & (32768))) || (v_46380.cljs$core$IDeref$))?true:(((!v_46380.cljs$lang$protocol_mask$partition0$))?cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46380):false)):cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46380))){
(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(v_46380) : cljs.core.deref.call(null,v_46380));
} else {
}

var G__46381 = cljs.core.next(seq__46358_46374__$1);
var G__46382 = null;
var G__46383 = (0);
var G__46384 = (0);
seq__46358_46364 = G__46381;
chunk__46359_46365 = G__46382;
count__46360_46366 = G__46383;
i__46361_46367 = G__46384;
continue;
}
} else {
}
}
break;
}

return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$canvas,cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(props,cljs.core.cst$kw$width,width,cljs.core.array_seq([cljs.core.cst$kw$height,height], 0))], null);
})], null));
});
org.numenta.sanity.helpers.window_resize_listener = (function org$numenta$sanity$helpers$window_resize_listener(resizes_c){

var resize_key = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
return reagent.core.create_class(new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$component_DASH_did_DASH_mount,((function (resize_key){
return (function (component){
var G__46397 = resize_key;
var G__46398 = (function (){var G__46399 = window;
var G__46400 = "resize";
var G__46401 = ((function (G__46399,G__46400,G__46397,resize_key){
return (function (){
return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(resizes_c,cljs.core.cst$kw$window_DASH_resized);
});})(G__46399,G__46400,G__46397,resize_key))
;
return goog.events.listen(G__46399,G__46400,G__46401);
})();
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__46397,G__46398) : cljs.core.reset_BANG_.call(null,G__46397,G__46398));
});})(resize_key))
,cljs.core.cst$kw$component_DASH_will_DASH_unmount,((function (resize_key){
return (function (){
if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(resize_key) : cljs.core.deref.call(null,resize_key)))){
var G__46402 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(resize_key) : cljs.core.deref.call(null,resize_key));
return goog.events.unlistenByKey(G__46402);
} else {
return null;
}
});})(resize_key))
,cljs.core.cst$kw$display_DASH_name,"window-resize-listener",cljs.core.cst$kw$reagent_DASH_render,((function (resize_key){
return (function (_){
return null;
});})(resize_key))
], null));
});
org.numenta.sanity.helpers.resizing_canvas$call_draw_fn = (function org$numenta$sanity$helpers$resizing_canvas$call_draw_fn(component){
var vec__46405 = reagent.core.argv(component);
var _ = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46405,(0),null);
var ___$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46405,(1),null);
var ___$2 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46405,(2),null);
var draw = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46405,(3),null);
var ___$3 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__46405,(4),null);
var G__46406 = reagent.core.dom_node(component).getContext("2d");
return (draw.cljs$core$IFn$_invoke$arity$1 ? draw.cljs$core$IFn$_invoke$arity$1(G__46406) : draw.call(null,G__46406));
});
org.numenta.sanity.helpers.resizing_canvas = (function org$numenta$sanity$helpers$resizing_canvas(_,___$1,___$2,invalidates_c,resizes){

var width_px = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
var height_px = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
var invalidates_c__$1 = (function (){var or__6153__auto__ = invalidates_c;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
}
})();
var teardown_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
return reagent.core.create_class(new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$component_DASH_did_DASH_mount,((function (width_px,height_px,invalidates_c__$1,teardown_c){
return (function (component){
var c__38109__auto___46594 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___46594,width_px,height_px,invalidates_c__$1,teardown_c){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___46594,width_px,height_px,invalidates_c__$1,teardown_c){
return (function (state_46553){
var state_val_46554 = (state_46553[(1)]);
if((state_val_46554 === (7))){
var inst_46528 = (state_46553[(2)]);
var inst_46529 = (inst_46528 == null);
var inst_46530 = cljs.core.not(inst_46529);
var state_46553__$1 = state_46553;
if(inst_46530){
var statearr_46555_46595 = state_46553__$1;
(statearr_46555_46595[(1)] = (14));

} else {
var statearr_46556_46596 = state_46553__$1;
(statearr_46556_46596[(1)] = (15));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (1))){
var state_46553__$1 = state_46553;
var statearr_46557_46597 = state_46553__$1;
(statearr_46557_46597[(2)] = null);

(statearr_46557_46597[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (4))){
var inst_46513 = (state_46553[(7)]);
var inst_46511 = (state_46553[(2)]);
var inst_46512 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_46511,(0),null);
var inst_46513__$1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_46511,(1),null);
var inst_46514 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_46513__$1,teardown_c);
var state_46553__$1 = (function (){var statearr_46558 = state_46553;
(statearr_46558[(7)] = inst_46513__$1);

(statearr_46558[(8)] = inst_46512);

return statearr_46558;
})();
if(inst_46514){
var statearr_46559_46598 = state_46553__$1;
(statearr_46559_46598[(1)] = (5));

} else {
var statearr_46560_46599 = state_46553__$1;
(statearr_46560_46599[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (15))){
var state_46553__$1 = state_46553;
var statearr_46561_46600 = state_46553__$1;
(statearr_46561_46600[(2)] = null);

(statearr_46561_46600[(1)] = (16));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (13))){
var inst_46524 = (state_46553[(2)]);
var state_46553__$1 = state_46553;
var statearr_46562_46601 = state_46553__$1;
(statearr_46562_46601[(2)] = inst_46524);

(statearr_46562_46601[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (6))){
var inst_46513 = (state_46553[(7)]);
var inst_46517 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_46513,invalidates_c__$1);
var state_46553__$1 = state_46553;
if(inst_46517){
var statearr_46563_46602 = state_46553__$1;
(statearr_46563_46602[(1)] = (8));

} else {
var statearr_46564_46603 = state_46553__$1;
(statearr_46564_46603[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (17))){
var inst_46534 = (state_46553[(9)]);
var inst_46535 = (state_46553[(10)]);
var inst_46539 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_46540 = [inst_46534,inst_46535];
var inst_46541 = (new cljs.core.PersistentVector(null,2,(5),inst_46539,inst_46540,null));
var inst_46542 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(resizes,inst_46541);
var state_46553__$1 = state_46553;
var statearr_46565_46604 = state_46553__$1;
(statearr_46565_46604[(2)] = inst_46542);

(statearr_46565_46604[(1)] = (19));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (3))){
var inst_46551 = (state_46553[(2)]);
var state_46553__$1 = state_46553;
return cljs.core.async.impl.ioc_helpers.return_chan(state_46553__$1,inst_46551);
} else {
if((state_val_46554 === (12))){
var state_46553__$1 = state_46553;
var statearr_46566_46605 = state_46553__$1;
(statearr_46566_46605[(2)] = null);

(statearr_46566_46605[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (2))){
var inst_46507 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_46508 = [teardown_c,invalidates_c__$1];
var inst_46509 = (new cljs.core.PersistentVector(null,2,(5),inst_46507,inst_46508,null));
var state_46553__$1 = state_46553;
return cljs.core.async.ioc_alts_BANG_.cljs$core$IFn$_invoke$arity$variadic(state_46553__$1,(4),inst_46509,cljs.core.array_seq([cljs.core.cst$kw$priority,true], 0));
} else {
if((state_val_46554 === (19))){
var inst_46545 = (state_46553[(2)]);
var state_46553__$1 = (function (){var statearr_46567 = state_46553;
(statearr_46567[(11)] = inst_46545);

return statearr_46567;
})();
var statearr_46568_46606 = state_46553__$1;
(statearr_46568_46606[(2)] = null);

(statearr_46568_46606[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (11))){
var inst_46512 = (state_46553[(8)]);
var state_46553__$1 = state_46553;
var statearr_46569_46607 = state_46553__$1;
(statearr_46569_46607[(2)] = inst_46512);

(statearr_46569_46607[(1)] = (13));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (9))){
var inst_46513 = (state_46553[(7)]);
var inst_46520 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_46513,cljs.core.cst$kw$default);
var state_46553__$1 = state_46553;
if(inst_46520){
var statearr_46570_46608 = state_46553__$1;
(statearr_46570_46608[(1)] = (11));

} else {
var statearr_46571_46609 = state_46553__$1;
(statearr_46571_46609[(1)] = (12));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (5))){
var state_46553__$1 = state_46553;
var statearr_46572_46610 = state_46553__$1;
(statearr_46572_46610[(2)] = null);

(statearr_46572_46610[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (14))){
var inst_46534 = (state_46553[(9)]);
var inst_46535 = (state_46553[(10)]);
var inst_46532 = reagent.core.dom_node(component);
var inst_46533 = goog.style.getSize(inst_46532);
var inst_46534__$1 = inst_46533.width;
var inst_46535__$1 = inst_46533.height;
var inst_46536 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(width_px,inst_46534__$1) : cljs.core.reset_BANG_.call(null,width_px,inst_46534__$1));
var inst_46537 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(height_px,inst_46535__$1) : cljs.core.reset_BANG_.call(null,height_px,inst_46535__$1));
var state_46553__$1 = (function (){var statearr_46573 = state_46553;
(statearr_46573[(9)] = inst_46534__$1);

(statearr_46573[(12)] = inst_46537);

(statearr_46573[(13)] = inst_46536);

(statearr_46573[(10)] = inst_46535__$1);

return statearr_46573;
})();
if(cljs.core.truth_(resizes)){
var statearr_46574_46611 = state_46553__$1;
(statearr_46574_46611[(1)] = (17));

} else {
var statearr_46575_46612 = state_46553__$1;
(statearr_46575_46612[(1)] = (18));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (16))){
var inst_46549 = (state_46553[(2)]);
var state_46553__$1 = state_46553;
var statearr_46576_46613 = state_46553__$1;
(statearr_46576_46613[(2)] = inst_46549);

(statearr_46576_46613[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (10))){
var inst_46526 = (state_46553[(2)]);
var state_46553__$1 = state_46553;
var statearr_46577_46614 = state_46553__$1;
(statearr_46577_46614[(2)] = inst_46526);

(statearr_46577_46614[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (18))){
var state_46553__$1 = state_46553;
var statearr_46578_46615 = state_46553__$1;
(statearr_46578_46615[(2)] = null);

(statearr_46578_46615[(1)] = (19));


return cljs.core.cst$kw$recur;
} else {
if((state_val_46554 === (8))){
var state_46553__$1 = state_46553;
var statearr_46579_46616 = state_46553__$1;
(statearr_46579_46616[(2)] = true);

(statearr_46579_46616[(1)] = (10));


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
}
}
}
}
}
}
}
}
}
}
});})(c__38109__auto___46594,width_px,height_px,invalidates_c__$1,teardown_c))
;
return ((function (switch__37995__auto__,c__38109__auto___46594,width_px,height_px,invalidates_c__$1,teardown_c){
return (function() {
var org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto____0 = (function (){
var statearr_46583 = [null,null,null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_46583[(0)] = org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto__);

(statearr_46583[(1)] = (1));

return statearr_46583;
});
var org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto____1 = (function (state_46553){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_46553);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e46584){if((e46584 instanceof Object)){
var ex__37999__auto__ = e46584;
var statearr_46585_46617 = state_46553;
(statearr_46585_46617[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_46553);

return cljs.core.cst$kw$recur;
} else {
throw e46584;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__46618 = state_46553;
state_46553 = G__46618;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto__ = function(state_46553){
switch(arguments.length){
case 0:
return org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto____1.call(this,state_46553);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto____0;
org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto____1;
return org$numenta$sanity$helpers$resizing_canvas_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___46594,width_px,height_px,invalidates_c__$1,teardown_c))
})();
var state__38111__auto__ = (function (){var statearr_46586 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_46586[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___46594);

return statearr_46586;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___46594,width_px,height_px,invalidates_c__$1,teardown_c))
);


return cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(invalidates_c__$1,cljs.core.cst$kw$initial_DASH_mount);
});})(width_px,height_px,invalidates_c__$1,teardown_c))
,cljs.core.cst$kw$component_DASH_did_DASH_update,((function (width_px,height_px,invalidates_c__$1,teardown_c){
return (function (p1__46407_SHARP_){
return org.numenta.sanity.helpers.resizing_canvas$call_draw_fn(p1__46407_SHARP_);
});})(width_px,height_px,invalidates_c__$1,teardown_c))
,cljs.core.cst$kw$component_DASH_will_DASH_unmount,((function (width_px,height_px,invalidates_c__$1,teardown_c){
return (function (){
return cljs.core.async.close_BANG_(teardown_c);
});})(width_px,height_px,invalidates_c__$1,teardown_c))
,cljs.core.cst$kw$display_DASH_name,"resizing-canvas",cljs.core.cst$kw$reagent_DASH_render,((function (width_px,height_px,invalidates_c__$1,teardown_c){
return (function (props,canaries,___$3,___$4){
var seq__46587_46619 = cljs.core.seq(canaries);
var chunk__46588_46620 = null;
var count__46589_46621 = (0);
var i__46590_46622 = (0);
while(true){
if((i__46590_46622 < count__46589_46621)){
var v_46623 = chunk__46588_46620.cljs$core$IIndexed$_nth$arity$2(null,i__46590_46622);
if(((!((v_46623 == null)))?((((v_46623.cljs$lang$protocol_mask$partition0$ & (32768))) || (v_46623.cljs$core$IDeref$))?true:(((!v_46623.cljs$lang$protocol_mask$partition0$))?cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46623):false)):cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46623))){
(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(v_46623) : cljs.core.deref.call(null,v_46623));
} else {
}

var G__46624 = seq__46587_46619;
var G__46625 = chunk__46588_46620;
var G__46626 = count__46589_46621;
var G__46627 = (i__46590_46622 + (1));
seq__46587_46619 = G__46624;
chunk__46588_46620 = G__46625;
count__46589_46621 = G__46626;
i__46590_46622 = G__46627;
continue;
} else {
var temp__4657__auto___46628 = cljs.core.seq(seq__46587_46619);
if(temp__4657__auto___46628){
var seq__46587_46629__$1 = temp__4657__auto___46628;
if(cljs.core.chunked_seq_QMARK_(seq__46587_46629__$1)){
var c__6956__auto___46630 = cljs.core.chunk_first(seq__46587_46629__$1);
var G__46631 = cljs.core.chunk_rest(seq__46587_46629__$1);
var G__46632 = c__6956__auto___46630;
var G__46633 = cljs.core.count(c__6956__auto___46630);
var G__46634 = (0);
seq__46587_46619 = G__46631;
chunk__46588_46620 = G__46632;
count__46589_46621 = G__46633;
i__46590_46622 = G__46634;
continue;
} else {
var v_46635 = cljs.core.first(seq__46587_46629__$1);
if(((!((v_46635 == null)))?((((v_46635.cljs$lang$protocol_mask$partition0$ & (32768))) || (v_46635.cljs$core$IDeref$))?true:(((!v_46635.cljs$lang$protocol_mask$partition0$))?cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46635):false)):cljs.core.native_satisfies_QMARK_(cljs.core.IDeref,v_46635))){
(cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(v_46635) : cljs.core.deref.call(null,v_46635));
} else {
}

var G__46636 = cljs.core.next(seq__46587_46629__$1);
var G__46637 = null;
var G__46638 = (0);
var G__46639 = (0);
seq__46587_46619 = G__46636;
chunk__46588_46620 = G__46637;
count__46589_46621 = G__46638;
i__46590_46622 = G__46639;
continue;
}
} else {
}
}
break;
}

var w = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(width_px) : cljs.core.deref.call(null,width_px));
var h = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(height_px) : cljs.core.deref.call(null,height_px));
if(((w === (0))) || ((h === (0)))){
var G__46593_46640 = [cljs.core.str("The resizing canvas is size "),cljs.core.str(w),cljs.core.str(" "),cljs.core.str(h),cljs.core.str(". If it's 'display:none`, it won't detect "),cljs.core.str("its own visibility change.")].join('');
console.warn(G__46593_46640);
} else {
}

return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$canvas,cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(props,cljs.core.cst$kw$width,w,cljs.core.array_seq([cljs.core.cst$kw$height,h], 0))], null);
});})(width_px,height_px,invalidates_c__$1,teardown_c))
], null));
});
