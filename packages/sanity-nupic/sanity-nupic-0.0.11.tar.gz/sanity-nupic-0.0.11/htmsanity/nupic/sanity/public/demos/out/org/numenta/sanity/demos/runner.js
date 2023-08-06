// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.runner');
goog.require('cljs.core');
goog.require('goog.dom');
goog.require('reagent.core');
goog.require('org.numenta.sanity.main');
goog.require('org.numenta.sanity.bridge.remote');
goog.require('org.numenta.sanity.util');
goog.require('cljs.core.async');
org.numenta.sanity.demos.runner.key_value_display = (function org$numenta$sanity$demos$runner$key_value_display(k,v){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$margin_DASH_top,(20)], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$font_DASH_family,"sans-serif",cljs.core.cst$kw$font_DASH_size,"9px",cljs.core.cst$kw$font_DASH_weight,"bold"], null)], null),k], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$strong,v], null)], null)], null);
});
org.numenta.sanity.demos.runner.world_pane = (function org$numenta$sanity$demos$runner$world_pane(steps,selection){
if(cljs.core.truth_(cljs.core.not_empty((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(steps) : cljs.core.deref.call(null,steps))))){
var step = org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$2(steps,selection);
var kvs = (function (){var temp__4655__auto__ = cljs.core.cst$kw$display_DASH_value.cljs$core$IFn$_invoke$arity$1(step);
if(cljs.core.truth_(temp__4655__auto__)){
var display_value = temp__4655__auto__;
return cljs.core.seq(display_value);
} else {
if(cljs.core.truth_(cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(step))){
var iter__6925__auto__ = ((function (temp__4655__auto__,step){
return (function org$numenta$sanity$demos$runner$world_pane_$_iter__68229(s__68230){
return (new cljs.core.LazySeq(null,((function (temp__4655__auto__,step){
return (function (){
var s__68230__$1 = s__68230;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__68230__$1);
if(temp__4657__auto__){
var s__68230__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__68230__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__68230__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__68232 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__68231 = (0);
while(true){
if((i__68231 < size__6924__auto__)){
var vec__68237 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__68231);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68237,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68237,(1),null);
cljs.core.chunk_append(b__68232,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.name(sense_id),[cljs.core.str(v)].join('')], null));

var G__68249 = (i__68231 + (1));
i__68231 = G__68249;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__68232),org$numenta$sanity$demos$runner$world_pane_$_iter__68229(cljs.core.chunk_rest(s__68230__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__68232),null);
}
} else {
var vec__68238 = cljs.core.first(s__68230__$2);
var sense_id = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68238,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68238,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.name(sense_id),[cljs.core.str(v)].join('')], null),org$numenta$sanity$demos$runner$world_pane_$_iter__68229(cljs.core.rest(s__68230__$2)));
}
} else {
return null;
}
break;
}
});})(temp__4655__auto__,step))
,null,null));
});})(temp__4655__auto__,step))
;
return iter__6925__auto__(cljs.core.cst$kw$sensed_DASH_values.cljs$core$IFn$_invoke$arity$1(step));
} else {
return null;
}
}
})();
return cljs.core.into.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div], null),(function (){var iter__6925__auto__ = ((function (step,kvs){
return (function org$numenta$sanity$demos$runner$world_pane_$_iter__68239(s__68240){
return (new cljs.core.LazySeq(null,((function (step,kvs){
return (function (){
var s__68240__$1 = s__68240;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__68240__$1);
if(temp__4657__auto__){
var s__68240__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__68240__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__68240__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__68242 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__68241 = (0);
while(true){
if((i__68241 < size__6924__auto__)){
var vec__68247 = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__68241);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68247,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68247,(1),null);
cljs.core.chunk_append(b__68242,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.runner.key_value_display,k,v], null));

var G__68250 = (i__68241 + (1));
i__68241 = G__68250;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__68242),org$numenta$sanity$demos$runner$world_pane_$_iter__68239(cljs.core.chunk_rest(s__68240__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__68242),null);
}
} else {
var vec__68248 = cljs.core.first(s__68240__$2);
var k = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68248,(0),null);
var v = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__68248,(1),null);
return cljs.core.cons(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.runner.key_value_display,k,v], null),org$numenta$sanity$demos$runner$world_pane_$_iter__68239(cljs.core.rest(s__68240__$2)));
}
} else {
return null;
}
break;
}
});})(step,kvs))
,null,null));
});})(step,kvs))
;
return iter__6925__auto__(kvs);
})());
} else {
return null;
}
});
org.numenta.sanity.demos.runner.init = (function org$numenta$sanity$demos$runner$init(var_args){
var args__7218__auto__ = [];
var len__7211__auto___68289 = arguments.length;
var i__7212__auto___68290 = (0);
while(true){
if((i__7212__auto___68290 < len__7211__auto___68289)){
args__7218__auto__.push((arguments[i__7212__auto___68290]));

var G__68291 = (i__7212__auto___68290 + (1));
i__7212__auto___68290 = G__68291;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((3) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((3)),(0))):null);
return org.numenta.sanity.demos.runner.init.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),argseq__7219__auto__);
});
goog.exportSymbol('org.numenta.sanity.demos.runner.init', org.numenta.sanity.demos.runner.init);

org.numenta.sanity.demos.runner.init.cljs$core$IFn$_invoke$arity$variadic = (function (title,ws_url,selected_tab,feature_list){
var into_sim_in = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
var into_sim_mult = cljs.core.async.mult(into_sim_in);
var into_sim_eavesdrop = org.numenta.sanity.util.tap_c(into_sim_mult);
var into_journal = org.numenta.sanity.main.into_journal;
var pipe_to_remote_target_BANG_ = org.numenta.sanity.bridge.remote.init(ws_url);
var features = cljs.core.into.cljs$core$IFn$_invoke$arity$3(cljs.core.PersistentHashSet.EMPTY,cljs.core.map.cljs$core$IFn$_invoke$arity$1(cljs.core.keyword),feature_list);
var current_tab = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.keyword.cljs$core$IFn$_invoke$arity$1(selected_tab));
(pipe_to_remote_target_BANG_.cljs$core$IFn$_invoke$arity$2 ? pipe_to_remote_target_BANG_.cljs$core$IFn$_invoke$arity$2("journal",into_journal) : pipe_to_remote_target_BANG_.call(null,"journal",into_journal));

var G__68255_68292 = "simulation";
var G__68256_68293 = org.numenta.sanity.util.tap_c(into_sim_mult);
(pipe_to_remote_target_BANG_.cljs$core$IFn$_invoke$arity$2 ? pipe_to_remote_target_BANG_.cljs$core$IFn$_invoke$arity$2(G__68255_68292,G__68256_68293) : pipe_to_remote_target_BANG_.call(null,G__68255_68292,G__68256_68293));

var c__38109__auto___68294 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___68294,into_sim_in,into_sim_mult,into_sim_eavesdrop,into_journal,pipe_to_remote_target_BANG_,features,current_tab){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___68294,into_sim_in,into_sim_mult,into_sim_eavesdrop,into_journal,pipe_to_remote_target_BANG_,features,current_tab){
return (function (state_68273){
var state_val_68274 = (state_68273[(1)]);
if((state_val_68274 === (1))){
var state_68273__$1 = state_68273;
var statearr_68275_68295 = state_68273__$1;
(statearr_68275_68295[(2)] = null);

(statearr_68275_68295[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68274 === (2))){
var state_68273__$1 = state_68273;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_68273__$1,(4),into_sim_eavesdrop);
} else {
if((state_val_68274 === (3))){
var inst_68271 = (state_68273[(2)]);
var state_68273__$1 = state_68273;
return cljs.core.async.impl.ioc_helpers.return_chan(state_68273__$1,inst_68271);
} else {
if((state_val_68274 === (4))){
var inst_68259 = (state_68273[(2)]);
var inst_68260 = (inst_68259 == null);
var state_68273__$1 = state_68273;
if(cljs.core.truth_(inst_68260)){
var statearr_68276_68296 = state_68273__$1;
(statearr_68276_68296[(1)] = (5));

} else {
var statearr_68277_68297 = state_68273__$1;
(statearr_68277_68297[(1)] = (6));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_68274 === (5))){
var state_68273__$1 = state_68273;
var statearr_68278_68298 = state_68273__$1;
(statearr_68278_68298[(2)] = null);

(statearr_68278_68298[(1)] = (7));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68274 === (6))){
var inst_68263 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_68264 = ["ping"];
var inst_68265 = (new cljs.core.PersistentVector(null,1,(5),inst_68263,inst_68264,null));
var inst_68266 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(into_journal,inst_68265);
var state_68273__$1 = (function (){var statearr_68279 = state_68273;
(statearr_68279[(7)] = inst_68266);

return statearr_68279;
})();
var statearr_68280_68299 = state_68273__$1;
(statearr_68280_68299[(2)] = null);

(statearr_68280_68299[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_68274 === (7))){
var inst_68269 = (state_68273[(2)]);
var state_68273__$1 = state_68273;
var statearr_68281_68300 = state_68273__$1;
(statearr_68281_68300[(2)] = inst_68269);

(statearr_68281_68300[(1)] = (3));


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
});})(c__38109__auto___68294,into_sim_in,into_sim_mult,into_sim_eavesdrop,into_journal,pipe_to_remote_target_BANG_,features,current_tab))
;
return ((function (switch__37995__auto__,c__38109__auto___68294,into_sim_in,into_sim_mult,into_sim_eavesdrop,into_journal,pipe_to_remote_target_BANG_,features,current_tab){
return (function() {
var org$numenta$sanity$demos$runner$state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$runner$state_machine__37996__auto____0 = (function (){
var statearr_68285 = [null,null,null,null,null,null,null,null];
(statearr_68285[(0)] = org$numenta$sanity$demos$runner$state_machine__37996__auto__);

(statearr_68285[(1)] = (1));

return statearr_68285;
});
var org$numenta$sanity$demos$runner$state_machine__37996__auto____1 = (function (state_68273){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_68273);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e68286){if((e68286 instanceof Object)){
var ex__37999__auto__ = e68286;
var statearr_68287_68301 = state_68273;
(statearr_68287_68301[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_68273);

return cljs.core.cst$kw$recur;
} else {
throw e68286;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__68302 = state_68273;
state_68273 = G__68302;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$runner$state_machine__37996__auto__ = function(state_68273){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$runner$state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$runner$state_machine__37996__auto____1.call(this,state_68273);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$runner$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$runner$state_machine__37996__auto____0;
org$numenta$sanity$demos$runner$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$runner$state_machine__37996__auto____1;
return org$numenta$sanity$demos$runner$state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___68294,into_sim_in,into_sim_mult,into_sim_eavesdrop,into_journal,pipe_to_remote_target_BANG_,features,current_tab))
})();
var state__38111__auto__ = (function (){var statearr_68288 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_68288[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___68294);

return statearr_68288;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___68294,into_sim_in,into_sim_mult,into_sim_eavesdrop,into_journal,pipe_to_remote_target_BANG_,features,current_tab))
);


return reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,title,null,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.runner.world_pane,org.numenta.sanity.main.steps,org.numenta.sanity.main.selection], null),current_tab,features,into_sim_in], null),goog.dom.getElement("sanity-app"));
});

org.numenta.sanity.demos.runner.init.cljs$lang$maxFixedArity = (3);

org.numenta.sanity.demos.runner.init.cljs$lang$applyTo = (function (seq68251){
var G__68252 = cljs.core.first(seq68251);
var seq68251__$1 = cljs.core.next(seq68251);
var G__68253 = cljs.core.first(seq68251__$1);
var seq68251__$2 = cljs.core.next(seq68251__$1);
var G__68254 = cljs.core.first(seq68251__$2);
var seq68251__$3 = cljs.core.next(seq68251__$2);
return org.numenta.sanity.demos.runner.init.cljs$core$IFn$_invoke$arity$variadic(G__68252,G__68253,G__68254,seq68251__$3);
});
