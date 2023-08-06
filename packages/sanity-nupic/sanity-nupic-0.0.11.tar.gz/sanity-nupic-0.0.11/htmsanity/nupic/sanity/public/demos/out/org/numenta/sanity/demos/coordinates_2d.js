// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.coordinates_2d');
goog.require('cljs.core');
goog.require('org.numenta.sanity.plots_canvas');
goog.require('goog.dom');
goog.require('reagent.core');
goog.require('org.numenta.sanity.helpers');
goog.require('org.numenta.sanity.main');
goog.require('org.nfrac.comportex.demos.coordinates_2d');
goog.require('org.numenta.sanity.util');
goog.require('org.numenta.sanity.comportex.data');
goog.require('cljs.core.async');
goog.require('reagent_forms.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.numenta.sanity.bridge.browser');
goog.require('org.numenta.sanity.demos.comportex_common');
goog.require('org.nfrac.comportex.util');
goog.require('monet.canvas');
org.numenta.sanity.demos.coordinates_2d.config = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$n_DASH_regions,(1)], null));
org.numenta.sanity.demos.coordinates_2d.quadrant = (function org$numenta$sanity$demos$coordinates_2d$quadrant(inval){
return [cljs.core.str((((cljs.core.cst$kw$y.cljs$core$IFn$_invoke$arity$1(inval) > (0)))?"S":"N")),cljs.core.str((((cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(inval) > (0)))?"E":"W"))].join('');
});
org.numenta.sanity.demos.coordinates_2d.world_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$2(cljs.core.async.buffer((1)),cljs.core.comp.cljs$core$IFn$_invoke$arity$2(cljs.core.map.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.util.keep_history_middleware((50),(function (p1__72625_SHARP_){
return cljs.core.select_keys(p1__72625_SHARP_,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$x,cljs.core.cst$kw$y,cljs.core.cst$kw$vx,cljs.core.cst$kw$vy], null));
}),cljs.core.cst$kw$history)),cljs.core.map.cljs$core$IFn$_invoke$arity$1((function (p1__72626_SHARP_){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__72626_SHARP_,cljs.core.cst$kw$label,org.numenta.sanity.demos.coordinates_2d.quadrant(p1__72626_SHARP_));
}))));
org.numenta.sanity.demos.coordinates_2d.model = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
org.numenta.sanity.demos.coordinates_2d.into_sim = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.demos.coordinates_2d.control_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
/**
 * Feed the world channel continuously, reacting to UI settings.
 */
org.numenta.sanity.demos.coordinates_2d.feed_world_BANG_ = (function org$numenta$sanity$demos$coordinates_2d$feed_world_BANG_(){
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__){
return (function (state_72707){
var state_val_72708 = (state_72707[(1)]);
if((state_val_72708 === (7))){
var inst_72690 = (state_72707[(2)]);
var inst_72691 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_72690,(0),null);
var inst_72692 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(inst_72690,(1),null);
var inst_72693 = cljs.core._EQ_.cljs$core$IFn$_invoke$arity$2(inst_72692,org.numenta.sanity.demos.coordinates_2d.control_c);
var state_72707__$1 = (function (){var statearr_72709 = state_72707;
(statearr_72709[(7)] = inst_72691);

return statearr_72709;
})();
if(inst_72693){
var statearr_72710_72729 = state_72707__$1;
(statearr_72710_72729[(1)] = (8));

} else {
var statearr_72711_72730 = state_72707__$1;
(statearr_72711_72730[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_72708 === (1))){
var inst_72678 = org.nfrac.comportex.demos.coordinates_2d.initial_input_val;
var state_72707__$1 = (function (){var statearr_72712 = state_72707;
(statearr_72712[(8)] = inst_72678);

return statearr_72712;
})();
var statearr_72713_72731 = state_72707__$1;
(statearr_72713_72731[(2)] = null);

(statearr_72713_72731[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72708 === (4))){
var inst_72678 = (state_72707[(8)]);
var inst_72681 = (state_72707[(2)]);
var inst_72682 = cljs.core.async.timeout((50));
var inst_72683 = inst_72678;
var state_72707__$1 = (function (){var statearr_72714 = state_72707;
(statearr_72714[(9)] = inst_72682);

(statearr_72714[(10)] = inst_72683);

(statearr_72714[(11)] = inst_72681);

return statearr_72714;
})();
var statearr_72715_72732 = state_72707__$1;
(statearr_72715_72732[(2)] = null);

(statearr_72715_72732[(1)] = (5));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72708 === (6))){
var inst_72701 = (state_72707[(2)]);
var inst_72702 = org.nfrac.comportex.demos.coordinates_2d.input_transform(inst_72701);
var inst_72678 = inst_72702;
var state_72707__$1 = (function (){var statearr_72716 = state_72707;
(statearr_72716[(8)] = inst_72678);

return statearr_72716;
})();
var statearr_72717_72733 = state_72707__$1;
(statearr_72717_72733[(2)] = null);

(statearr_72717_72733[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72708 === (3))){
var inst_72705 = (state_72707[(2)]);
var state_72707__$1 = state_72707;
return cljs.core.async.impl.ioc_helpers.return_chan(state_72707__$1,inst_72705);
} else {
if((state_val_72708 === (2))){
var inst_72678 = (state_72707[(8)]);
var state_72707__$1 = state_72707;
return cljs.core.async.impl.ioc_helpers.put_BANG_(state_72707__$1,(4),org.numenta.sanity.demos.coordinates_2d.world_c,inst_72678);
} else {
if((state_val_72708 === (9))){
var inst_72683 = (state_72707[(10)]);
var state_72707__$1 = state_72707;
var statearr_72718_72734 = state_72707__$1;
(statearr_72718_72734[(2)] = inst_72683);

(statearr_72718_72734[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72708 === (5))){
var inst_72682 = (state_72707[(9)]);
var inst_72686 = cljs.core.PersistentVector.EMPTY_NODE;
var inst_72687 = [org.numenta.sanity.demos.coordinates_2d.control_c,inst_72682];
var inst_72688 = (new cljs.core.PersistentVector(null,2,(5),inst_72686,inst_72687,null));
var state_72707__$1 = state_72707;
return cljs.core.async.ioc_alts_BANG_(state_72707__$1,(7),inst_72688);
} else {
if((state_val_72708 === (10))){
var inst_72699 = (state_72707[(2)]);
var state_72707__$1 = state_72707;
var statearr_72719_72735 = state_72707__$1;
(statearr_72719_72735[(2)] = inst_72699);

(statearr_72719_72735[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72708 === (8))){
var inst_72683 = (state_72707[(10)]);
var inst_72691 = (state_72707[(7)]);
var inst_72695 = (inst_72691.cljs$core$IFn$_invoke$arity$1 ? inst_72691.cljs$core$IFn$_invoke$arity$1(inst_72683) : inst_72691.call(null,inst_72683));
var inst_72683__$1 = inst_72695;
var state_72707__$1 = (function (){var statearr_72720 = state_72707;
(statearr_72720[(10)] = inst_72683__$1);

return statearr_72720;
})();
var statearr_72721_72736 = state_72707__$1;
(statearr_72721_72736[(2)] = null);

(statearr_72721_72736[(1)] = (5));


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
});})(c__38109__auto__))
;
return ((function (switch__37995__auto__,c__38109__auto__){
return (function() {
var org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_72725 = [null,null,null,null,null,null,null,null,null,null,null,null];
(statearr_72725[(0)] = org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto__);

(statearr_72725[(1)] = (1));

return statearr_72725;
});
var org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto____1 = (function (state_72707){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_72707);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e72726){if((e72726 instanceof Object)){
var ex__37999__auto__ = e72726;
var statearr_72727_72737 = state_72707;
(statearr_72727_72737[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_72707);

return cljs.core.cst$kw$recur;
} else {
throw e72726;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__72738 = state_72707;
state_72707 = G__72738;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto__ = function(state_72707){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto____1.call(this,state_72707);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$coordinates_2d$feed_world_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__))
})();
var state__38111__auto__ = (function (){var statearr_72728 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_72728[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_72728;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__))
);

return c__38109__auto__;
});
org.numenta.sanity.demos.coordinates_2d.draw_arrow = (function org$numenta$sanity$demos$coordinates_2d$draw_arrow(ctx,p__72739){
var map__72742 = p__72739;
var map__72742__$1 = ((((!((map__72742 == null)))?((((map__72742.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72742.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72742):map__72742);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72742__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72742__$1,cljs.core.cst$kw$y);
var angle = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72742__$1,cljs.core.cst$kw$angle);
monet.canvas.save(ctx);

monet.canvas.translate(ctx,x,y);

monet.canvas.rotate(ctx,angle);

monet.canvas.begin_path(ctx);

monet.canvas.move_to(ctx,(5),(0));

monet.canvas.line_to(ctx,(-5),(3));

monet.canvas.line_to(ctx,(-5),(-3));

monet.canvas.line_to(ctx,(5),(0));

monet.canvas.fill(ctx);

monet.canvas.stroke(ctx);

return monet.canvas.restore(ctx);
});
org.numenta.sanity.demos.coordinates_2d.centred_rect = (function org$numenta$sanity$demos$coordinates_2d$centred_rect(cx,cy,w,h){
return new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(cx - (w / (2))),cljs.core.cst$kw$y,(cy - (h / (2))),cljs.core.cst$kw$w,w,cljs.core.cst$kw$h,h], null);
});
org.numenta.sanity.demos.coordinates_2d.draw_world = (function org$numenta$sanity$demos$coordinates_2d$draw_world(ctx,in_value){
var max_pos = org.nfrac.comportex.demos.coordinates_2d.max_pos;
var radius = org.nfrac.comportex.demos.coordinates_2d.radius;
var x_lim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(- max_pos),max_pos], null);
var y_lim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(- max_pos),max_pos], null);
var width_px = ctx.canvas.width;
var height_px = ctx.canvas.height;
var edge_px = (function (){var x__6491__auto__ = width_px;
var y__6492__auto__ = height_px;
return ((x__6491__auto__ < y__6492__auto__) ? x__6491__auto__ : y__6492__auto__);
})();
var plot_size = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$w,edge_px,cljs.core.cst$kw$h,edge_px], null);
var plot = org.numenta.sanity.plots_canvas.xy_plot(ctx,plot_size,x_lim,y_lim);
var x_scale = org.numenta.sanity.plots_canvas.scale_fn(x_lim,cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(plot_size));
var y_scale = org.numenta.sanity.plots_canvas.scale_fn(y_lim,cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(plot_size));
var map__72756 = in_value;
var map__72756__$1 = ((((!((map__72756 == null)))?((((map__72756.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72756.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72756):map__72756);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72756__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72756__$1,cljs.core.cst$kw$y);
var vx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72756__$1,cljs.core.cst$kw$vx);
var vy = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72756__$1,cljs.core.cst$kw$vy);
var history = cljs.core.cst$kw$history.cljs$core$IFn$_invoke$arity$1(cljs.core.meta(in_value));
var r_px = ((x_scale.cljs$core$IFn$_invoke$arity$1 ? x_scale.cljs$core$IFn$_invoke$arity$1(radius) : x_scale.call(null,radius)) - (x_scale.cljs$core$IFn$_invoke$arity$1 ? x_scale.cljs$core$IFn$_invoke$arity$1((0)) : x_scale.call(null,(0))));
monet.canvas.clear_rect(ctx,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$w,width_px,cljs.core.cst$kw$h,height_px], null));

org.numenta.sanity.plots_canvas.frame_BANG_(plot);

monet.canvas.stroke_style(ctx,"lightgray");

org.numenta.sanity.plots_canvas.grid_BANG_(plot,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$grid_DASH_every,(2)], null));

monet.canvas.stroke_style(ctx,"black");

org.numenta.sanity.plots_canvas.draw_grid(ctx,cljs.core.map.cljs$core$IFn$_invoke$arity$2(x_scale,x_lim),cljs.core.map.cljs$core$IFn$_invoke$arity$2(y_scale,y_lim),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((x_scale.cljs$core$IFn$_invoke$arity$1 ? x_scale.cljs$core$IFn$_invoke$arity$1((0)) : x_scale.call(null,(0))))], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.nfrac.comportex.util.round.cljs$core$IFn$_invoke$arity$1((y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1((0)) : y_scale.call(null,(0))))], null));

monet.canvas.fill_style(ctx,"rgba(255,0,0,0.25)");

monet.canvas.fill_rect(ctx,org.numenta.sanity.demos.coordinates_2d.centred_rect((x_scale.cljs$core$IFn$_invoke$arity$1 ? x_scale.cljs$core$IFn$_invoke$arity$1(x) : x_scale.call(null,x)),(y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(y) : y_scale.call(null,y)),((2) * r_px),((2) * r_px)));

monet.canvas.stroke_style(ctx,"black");

monet.canvas.fill_style(ctx,"yellow");

var seq__72758 = cljs.core.seq(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,history));
var chunk__72759 = null;
var count__72760 = (0);
var i__72761 = (0);
while(true){
if((i__72761 < count__72760)){
var vec__72762 = chunk__72759.cljs$core$IIndexed$_nth$arity$2(null,i__72761);
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72762,(0),null);
var map__72763 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72762,(1),null);
var map__72763__$1 = ((((!((map__72763 == null)))?((((map__72763.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72763.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72763):map__72763);
var x__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72763__$1,cljs.core.cst$kw$x);
var y__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72763__$1,cljs.core.cst$kw$y);
var vx__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72763__$1,cljs.core.cst$kw$vx);
var vy__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72763__$1,cljs.core.cst$kw$vy);
if(((i + (1)) === cljs.core.count(history))){
monet.canvas.alpha(ctx,(1));
} else {
monet.canvas.alpha(ctx,(((i + (1)) / cljs.core.count(history)) / (2)));
}

org.numenta.sanity.demos.coordinates_2d.draw_arrow(ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,(x_scale.cljs$core$IFn$_invoke$arity$1 ? x_scale.cljs$core$IFn$_invoke$arity$1(x__$1) : x_scale.call(null,x__$1)),cljs.core.cst$kw$y,(y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(y__$1) : y_scale.call(null,y__$1)),cljs.core.cst$kw$angle,Math.atan2(vy__$1,vx__$1)], null));

var G__72768 = seq__72758;
var G__72769 = chunk__72759;
var G__72770 = count__72760;
var G__72771 = (i__72761 + (1));
seq__72758 = G__72768;
chunk__72759 = G__72769;
count__72760 = G__72770;
i__72761 = G__72771;
continue;
} else {
var temp__4657__auto__ = cljs.core.seq(seq__72758);
if(temp__4657__auto__){
var seq__72758__$1 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(seq__72758__$1)){
var c__6956__auto__ = cljs.core.chunk_first(seq__72758__$1);
var G__72772 = cljs.core.chunk_rest(seq__72758__$1);
var G__72773 = c__6956__auto__;
var G__72774 = cljs.core.count(c__6956__auto__);
var G__72775 = (0);
seq__72758 = G__72772;
chunk__72759 = G__72773;
count__72760 = G__72774;
i__72761 = G__72775;
continue;
} else {
var vec__72765 = cljs.core.first(seq__72758__$1);
var i = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72765,(0),null);
var map__72766 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72765,(1),null);
var map__72766__$1 = ((((!((map__72766 == null)))?((((map__72766.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72766.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72766):map__72766);
var x__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72766__$1,cljs.core.cst$kw$x);
var y__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72766__$1,cljs.core.cst$kw$y);
var vx__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72766__$1,cljs.core.cst$kw$vx);
var vy__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72766__$1,cljs.core.cst$kw$vy);
if(((i + (1)) === cljs.core.count(history))){
monet.canvas.alpha(ctx,(1));
} else {
monet.canvas.alpha(ctx,(((i + (1)) / cljs.core.count(history)) / (2)));
}

org.numenta.sanity.demos.coordinates_2d.draw_arrow(ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,(x_scale.cljs$core$IFn$_invoke$arity$1 ? x_scale.cljs$core$IFn$_invoke$arity$1(x__$1) : x_scale.call(null,x__$1)),cljs.core.cst$kw$y,(y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(y__$1) : y_scale.call(null,y__$1)),cljs.core.cst$kw$angle,Math.atan2(vy__$1,vx__$1)], null));

var G__72776 = cljs.core.next(seq__72758__$1);
var G__72777 = null;
var G__72778 = (0);
var G__72779 = (0);
seq__72758 = G__72776;
chunk__72759 = G__72777;
count__72760 = G__72778;
i__72761 = G__72779;
continue;
}
} else {
return null;
}
}
break;
}
});
org.numenta.sanity.demos.coordinates_2d.world_pane = (function org$numenta$sanity$demos$coordinates_2d$world_pane(){
var temp__4657__auto__ = org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0();
if(cljs.core.truth_(temp__4657__auto__)){
var step = temp__4657__auto__;
var in_value = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(step);
var map__72782 = in_value;
var map__72782__$1 = ((((!((map__72782 == null)))?((((map__72782.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72782.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72782):map__72782);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72782__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72782__$1,cljs.core.cst$kw$y);
var vx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72782__$1,cljs.core.cst$kw$vx);
var vy = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72782__$1,cljs.core.cst$kw$vy);
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$muted,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Input on selected timestep."], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$table$table,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"x"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,x], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"y"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,y], null)], null)], null),new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.helpers.resizing_canvas,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$width,"100%",cljs.core.cst$kw$height,"300px"], null)], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.selection], null),((function (in_value,map__72782,map__72782__$1,x,y,vx,vy,step,temp__4657__auto__){
return (function (ctx){
var step__$1 = org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0();
var in_value__$1 = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(step__$1);
return org.numenta.sanity.demos.coordinates_2d.draw_world(ctx,in_value__$1);
});})(in_value,map__72782,map__72782__$1,x,y,vx,vy,step,temp__4657__auto__))
,null], null)], null);
} else {
return null;
}
});
org.numenta.sanity.demos.coordinates_2d.set_model_BANG_ = (function org$numenta$sanity$demos$coordinates_2d$set_model_BANG_(){
return org.numenta.sanity.helpers.with_ui_loading_message((function (){
var init_QMARK_ = ((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.coordinates_2d.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.coordinates_2d.model)) == null);
var G__72788_72792 = org.numenta.sanity.demos.coordinates_2d.model;
var G__72789_72793 = org.nfrac.comportex.demos.coordinates_2d.n_region_model.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$n_DASH_regions.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.coordinates_2d.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.coordinates_2d.config))));
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__72788_72792,G__72789_72793) : cljs.core.reset_BANG_.call(null,G__72788_72792,G__72789_72793));

if(init_QMARK_){
org.numenta.sanity.bridge.browser.init.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.coordinates_2d.model,org.numenta.sanity.demos.coordinates_2d.world_c,org.numenta.sanity.main.into_journal,org.numenta.sanity.demos.coordinates_2d.into_sim);
} else {
var G__72790_72794 = org.numenta.sanity.main.network_shape;
var G__72791_72795 = org.numenta.sanity.util.translate_network_shape(org.numenta.sanity.comportex.data.network_shape((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.coordinates_2d.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.coordinates_2d.model))));
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__72790_72794,G__72791_72795) : cljs.core.reset_BANG_.call(null,G__72790_72794,G__72791_72795));
}

if(init_QMARK_){
return org.numenta.sanity.demos.coordinates_2d.feed_world_BANG_();
} else {
return null;
}
}));
});
org.numenta.sanity.demos.coordinates_2d.config_template = new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Number of regions:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$n_DASH_regions], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_offset_DASH_5$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.coordinates_2d.set_model_BANG_();

return e.preventDefault();
})], null),"Restart with new model"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_danger,"This resets all parameters."], null)], null)], null)], null);
org.numenta.sanity.demos.coordinates_2d.model_tab = (function org$numenta$sanity$demos$coordinates_2d$model_tab(){
return new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"A simple example of the coordinate encoder in 2\n    dimensions, on a repeating path."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"The coordinate is on a 90x90 integer grid and has a\n    locality radius of 15 units. It maintains position, velocity\n    and acceleration. Velocity is limited to 5 units per timestep.\n    When the point crosses the horizontal axis, its vertical\n    acceleration is reversed; when it crosses the vertical axis,\n    its horizontal acceleration is reversed."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"HTM model"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.bind_fields,org.numenta.sanity.demos.coordinates_2d.config_template,org.numenta.sanity.demos.coordinates_2d.config], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"Input"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label,"Interference with the movement path"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.coordinates_2d.control_c,(function (p1__72796_SHARP_){
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(p1__72796_SHARP_,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ay], null),cljs.core.dec);
}));

return e.preventDefault();
})], null),"Turn up"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.coordinates_2d.control_c,(function (p1__72797_SHARP_){
return cljs.core.update_in.cljs$core$IFn$_invoke$arity$3(p1__72797_SHARP_,new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ay], null),cljs.core.inc);
}));

return e.preventDefault();
})], null),"Turn down"], null)], null)], null)], null)], null);
});
org.numenta.sanity.demos.coordinates_2d.init = (function org$numenta$sanity$demos$coordinates_2d$init(){
reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,"Comportex",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.coordinates_2d.model_tab], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.coordinates_2d.world_pane], null),reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$model),org.numenta.sanity.demos.comportex_common.all_features,org.numenta.sanity.demos.coordinates_2d.into_sim], null),goog.dom.getElement("sanity-app"));

cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.main.viz_options,cljs.core.assoc_in,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$drawing,cljs.core.cst$kw$display_DASH_mode], null),cljs.core.cst$kw$two_DASH_d);

return org.numenta.sanity.demos.coordinates_2d.set_model_BANG_();
});
goog.exportSymbol('org.numenta.sanity.demos.coordinates_2d.init', org.numenta.sanity.demos.coordinates_2d.init);
