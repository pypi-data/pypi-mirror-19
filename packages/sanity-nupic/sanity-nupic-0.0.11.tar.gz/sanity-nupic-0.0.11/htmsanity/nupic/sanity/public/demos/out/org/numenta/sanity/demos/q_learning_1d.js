// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.q_learning_1d');
goog.require('cljs.core');
goog.require('org.numenta.sanity.plots_canvas');
goog.require('goog.dom');
goog.require('reagent.core');
goog.require('org.numenta.sanity.helpers');
goog.require('org.numenta.sanity.main');
goog.require('org.nfrac.comportex.demos.q_learning_1d');
goog.require('org.numenta.sanity.util');
goog.require('org.numenta.sanity.comportex.data');
goog.require('goog.string');
goog.require('cljs.core.async');
goog.require('org.numenta.sanity.bridge.marshalling');
goog.require('reagent_forms.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.numenta.sanity.bridge.browser');
goog.require('org.numenta.sanity.demos.comportex_common');
goog.require('org.nfrac.comportex.util');
goog.require('goog.string.format');
goog.require('monet.canvas');
org.numenta.sanity.demos.q_learning_1d.config = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$n_DASH_regions,(1)], null));
org.numenta.sanity.demos.q_learning_1d.world_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$2(cljs.core.async.buffer((1)),cljs.core.comp.cljs$core$IFn$_invoke$arity$2(cljs.core.map.cljs$core$IFn$_invoke$arity$1(org.nfrac.comportex.util.frequencies_middleware(cljs.core.cst$kw$x,cljs.core.cst$kw$freqs)),cljs.core.map.cljs$core$IFn$_invoke$arity$1((function (p1__72016_SHARP_){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__72016_SHARP_,cljs.core.cst$kw$label,cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(p1__72016_SHARP_));
}))));
org.numenta.sanity.demos.q_learning_1d.into_sim = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.demos.q_learning_1d.model = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
org.numenta.sanity.demos.q_learning_1d.draw_world = (function org$numenta$sanity$demos$q_learning_1d$draw_world(ctx,inval){
var surface = org.nfrac.comportex.demos.q_learning_1d.surface;
var surface_xy = cljs.core.mapv.cljs$core$IFn$_invoke$arity$3(cljs.core.vector,cljs.core.range.cljs$core$IFn$_invoke$arity$0(),surface);
var x_max = cljs.core.count(surface);
var y_max = cljs.core.reduce.cljs$core$IFn$_invoke$arity$2(cljs.core.max,surface);
var x_lim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [((0) - (1)),(x_max + (1))], null);
var y_lim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(y_max + (1)),(0)], null);
var width_px = ctx.canvas.width;
var height_px = ctx.canvas.height;
var plot_size = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$w,width_px,cljs.core.cst$kw$h,(100)], null);
monet.canvas.save(ctx);

monet.canvas.clear_rect(ctx,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$w,width_px,cljs.core.cst$kw$h,height_px], null));

var qplot_size_72061 = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$w,cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(plot_size),cljs.core.cst$kw$h,(40)], null);
var qplot_lim_72062 = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),(2)], null);
var qplot_72063 = org.numenta.sanity.plots_canvas.xy_plot(ctx,qplot_size_72061,x_lim,qplot_lim_72062);
org.numenta.sanity.plots_canvas.frame_BANG_(qplot_72063);

var seq__72039_72064 = cljs.core.seq(cljs.core.cst$kw$Q_DASH_map.cljs$core$IFn$_invoke$arity$1(inval));
var chunk__72041_72065 = null;
var count__72042_72066 = (0);
var i__72043_72067 = (0);
while(true){
if((i__72043_72067 < count__72042_72066)){
var vec__72045_72068 = chunk__72041_72065.cljs$core$IIndexed$_nth$arity$2(null,i__72043_72067);
var state_action_72069 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72045_72068,(0),null);
var q_72070 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72045_72068,(1),null);
var map__72046_72071 = state_action_72069;
var map__72046_72072__$1 = ((((!((map__72046_72071 == null)))?((((map__72046_72071.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72046_72071.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72046_72071):map__72046_72071);
var x_72073 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72046_72072__$1,cljs.core.cst$kw$x);
var action_72074 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72046_72072__$1,cljs.core.cst$kw$action);
var dx_72075 = cljs.core.cst$kw$dx.cljs$core$IFn$_invoke$arity$1(action_72074);
monet.canvas.fill_style(ctx,(((q_72070 > (0)))?"green":"red"));

monet.canvas.alpha(ctx,org.nfrac.comportex.util.abs(q_72070));

if((dx_72075 > (0))){
org.numenta.sanity.plots_canvas.rect_BANG_(qplot_72063,(x_72073 - 0.6),(0),0.6,(1));
} else {
if((dx_72075 < (0))){
org.numenta.sanity.plots_canvas.rect_BANG_(qplot_72063,x_72073,(1),0.6,(1));
} else {
}
}

var G__72076 = seq__72039_72064;
var G__72077 = chunk__72041_72065;
var G__72078 = count__72042_72066;
var G__72079 = (i__72043_72067 + (1));
seq__72039_72064 = G__72076;
chunk__72041_72065 = G__72077;
count__72042_72066 = G__72078;
i__72043_72067 = G__72079;
continue;
} else {
var temp__4657__auto___72080 = cljs.core.seq(seq__72039_72064);
if(temp__4657__auto___72080){
var seq__72039_72081__$1 = temp__4657__auto___72080;
if(cljs.core.chunked_seq_QMARK_(seq__72039_72081__$1)){
var c__6956__auto___72082 = cljs.core.chunk_first(seq__72039_72081__$1);
var G__72083 = cljs.core.chunk_rest(seq__72039_72081__$1);
var G__72084 = c__6956__auto___72082;
var G__72085 = cljs.core.count(c__6956__auto___72082);
var G__72086 = (0);
seq__72039_72064 = G__72083;
chunk__72041_72065 = G__72084;
count__72042_72066 = G__72085;
i__72043_72067 = G__72086;
continue;
} else {
var vec__72048_72087 = cljs.core.first(seq__72039_72081__$1);
var state_action_72088 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72048_72087,(0),null);
var q_72089 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72048_72087,(1),null);
var map__72049_72090 = state_action_72088;
var map__72049_72091__$1 = ((((!((map__72049_72090 == null)))?((((map__72049_72090.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72049_72090.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72049_72090):map__72049_72090);
var x_72092 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72049_72091__$1,cljs.core.cst$kw$x);
var action_72093 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72049_72091__$1,cljs.core.cst$kw$action);
var dx_72094 = cljs.core.cst$kw$dx.cljs$core$IFn$_invoke$arity$1(action_72093);
monet.canvas.fill_style(ctx,(((q_72089 > (0)))?"green":"red"));

monet.canvas.alpha(ctx,org.nfrac.comportex.util.abs(q_72089));

if((dx_72094 > (0))){
org.numenta.sanity.plots_canvas.rect_BANG_(qplot_72063,(x_72092 - 0.6),(0),0.6,(1));
} else {
if((dx_72094 < (0))){
org.numenta.sanity.plots_canvas.rect_BANG_(qplot_72063,x_72092,(1),0.6,(1));
} else {
}
}

var G__72095 = cljs.core.next(seq__72039_72081__$1);
var G__72096 = null;
var G__72097 = (0);
var G__72098 = (0);
seq__72039_72064 = G__72095;
chunk__72041_72065 = G__72096;
count__72042_72066 = G__72097;
i__72043_72067 = G__72098;
continue;
}
} else {
}
}
break;
}

monet.canvas.alpha(ctx,0.25);

monet.canvas.fill_style(ctx,"black");

var seq__72051_72099 = cljs.core.seq(cljs.core.range.cljs$core$IFn$_invoke$arity$1((cljs.core.count(surface) + (1))));
var chunk__72052_72100 = null;
var count__72053_72101 = (0);
var i__72054_72102 = (0);
while(true){
if((i__72054_72102 < count__72053_72101)){
var x_72103 = chunk__72052_72100.cljs$core$IIndexed$_nth$arity$2(null,i__72054_72102);
org.numenta.sanity.plots_canvas.line_BANG_(qplot_72063,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72103,(0)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72103,(2)], null)], null));

var G__72104 = seq__72051_72099;
var G__72105 = chunk__72052_72100;
var G__72106 = count__72053_72101;
var G__72107 = (i__72054_72102 + (1));
seq__72051_72099 = G__72104;
chunk__72052_72100 = G__72105;
count__72053_72101 = G__72106;
i__72054_72102 = G__72107;
continue;
} else {
var temp__4657__auto___72108 = cljs.core.seq(seq__72051_72099);
if(temp__4657__auto___72108){
var seq__72051_72109__$1 = temp__4657__auto___72108;
if(cljs.core.chunked_seq_QMARK_(seq__72051_72109__$1)){
var c__6956__auto___72110 = cljs.core.chunk_first(seq__72051_72109__$1);
var G__72111 = cljs.core.chunk_rest(seq__72051_72109__$1);
var G__72112 = c__6956__auto___72110;
var G__72113 = cljs.core.count(c__6956__auto___72110);
var G__72114 = (0);
seq__72051_72099 = G__72111;
chunk__72052_72100 = G__72112;
count__72053_72101 = G__72113;
i__72054_72102 = G__72114;
continue;
} else {
var x_72115 = cljs.core.first(seq__72051_72109__$1);
org.numenta.sanity.plots_canvas.line_BANG_(qplot_72063,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72115,(0)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72115,(2)], null)], null));

var G__72116 = cljs.core.next(seq__72051_72109__$1);
var G__72117 = null;
var G__72118 = (0);
var G__72119 = (0);
seq__72051_72099 = G__72116;
chunk__72052_72100 = G__72117;
count__72053_72101 = G__72118;
i__72054_72102 = G__72119;
continue;
}
} else {
}
}
break;
}

monet.canvas.alpha(ctx,(1));

monet.canvas.translate(ctx,(0),(40));

var plot_72120 = org.numenta.sanity.plots_canvas.xy_plot(ctx,plot_size,x_lim,y_lim);
org.numenta.sanity.plots_canvas.frame_BANG_(plot_72120);

monet.canvas.stroke_style(ctx,"lightgray");

org.numenta.sanity.plots_canvas.grid_BANG_(plot_72120,cljs.core.PersistentArrayMap.EMPTY);

monet.canvas.stroke_style(ctx,"black");

org.numenta.sanity.plots_canvas.line_BANG_(plot_72120,surface_xy);

var dx_1_72121 = cljs.core.cst$kw$dx.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$prev_DASH_action.cljs$core$IFn$_invoke$arity$1(inval));
var x_72122 = cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(inval);
var y_72123 = cljs.core.cst$kw$y.cljs$core$IFn$_invoke$arity$1(inval);
var x_1_72124 = (x_72122 - dx_1_72121);
var y_1_72125 = (surface.cljs$core$IFn$_invoke$arity$1 ? surface.cljs$core$IFn$_invoke$arity$1(x_1_72124) : surface.call(null,x_1_72124));
monet.canvas.stroke_style(ctx,"#888");

monet.canvas.fill_style(ctx,"white");

org.numenta.sanity.plots_canvas.point_BANG_(plot_72120,x_1_72124,y_1_72125,(3));

monet.canvas.stroke_style(ctx,"black");

monet.canvas.fill_style(ctx,"yellow");

org.numenta.sanity.plots_canvas.point_BANG_(plot_72120,x_72122,y_72123,(4));

monet.canvas.translate(ctx,(0),cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(plot_size));

var freqs_72126 = cljs.core.cst$kw$freqs.cljs$core$IFn$_invoke$arity$1(cljs.core.meta(inval));
var hist_lim_72127 = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),(cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.max,cljs.core.vals(freqs_72126)) + (1))], null);
var histogram_72128 = org.numenta.sanity.plots_canvas.xy_plot(ctx,plot_size,x_lim,hist_lim_72127);
monet.canvas.stroke_style(ctx,"black");

var seq__72055_72129 = cljs.core.seq(freqs_72126);
var chunk__72056_72130 = null;
var count__72057_72131 = (0);
var i__72058_72132 = (0);
while(true){
if((i__72058_72132 < count__72057_72131)){
var vec__72059_72133 = chunk__72056_72130.cljs$core$IIndexed$_nth$arity$2(null,i__72058_72132);
var x_72134 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72059_72133,(0),null);
var f_72135 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72059_72133,(1),null);
org.numenta.sanity.plots_canvas.line_BANG_(histogram_72128,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72134,(0)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72134,f_72135], null)], null));

var G__72136 = seq__72055_72129;
var G__72137 = chunk__72056_72130;
var G__72138 = count__72057_72131;
var G__72139 = (i__72058_72132 + (1));
seq__72055_72129 = G__72136;
chunk__72056_72130 = G__72137;
count__72057_72131 = G__72138;
i__72058_72132 = G__72139;
continue;
} else {
var temp__4657__auto___72140 = cljs.core.seq(seq__72055_72129);
if(temp__4657__auto___72140){
var seq__72055_72141__$1 = temp__4657__auto___72140;
if(cljs.core.chunked_seq_QMARK_(seq__72055_72141__$1)){
var c__6956__auto___72142 = cljs.core.chunk_first(seq__72055_72141__$1);
var G__72143 = cljs.core.chunk_rest(seq__72055_72141__$1);
var G__72144 = c__6956__auto___72142;
var G__72145 = cljs.core.count(c__6956__auto___72142);
var G__72146 = (0);
seq__72055_72129 = G__72143;
chunk__72056_72130 = G__72144;
count__72057_72131 = G__72145;
i__72058_72132 = G__72146;
continue;
} else {
var vec__72060_72147 = cljs.core.first(seq__72055_72141__$1);
var x_72148 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72060_72147,(0),null);
var f_72149 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72060_72147,(1),null);
org.numenta.sanity.plots_canvas.line_BANG_(histogram_72128,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72148,(0)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [x_72148,f_72149], null)], null));

var G__72150 = cljs.core.next(seq__72055_72141__$1);
var G__72151 = null;
var G__72152 = (0);
var G__72153 = (0);
seq__72055_72129 = G__72150;
chunk__72056_72130 = G__72151;
count__72057_72131 = G__72152;
i__72058_72132 = G__72153;
continue;
}
} else {
}
}
break;
}

return monet.canvas.restore(ctx);
});
org.numenta.sanity.demos.q_learning_1d.signed_str = (function org$numenta$sanity$demos$q_learning_1d$signed_str(x){
return [cljs.core.str((((x < (0)))?"":"+")),cljs.core.str(x)].join('');
});
org.numenta.sanity.demos.q_learning_1d.q_learning_sub_pane = (function org$numenta$sanity$demos$q_learning_1d$q_learning_sub_pane(htm){
var alyr = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(htm,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$regions,cljs.core.cst$kw$action,cljs.core.cst$kw$layer_DASH_3], null));
var qinfo = cljs.core.cst$kw$Q_DASH_info.cljs$core$IFn$_invoke$arity$1(alyr);
var map__72158 = cljs.core.cst$kw$spec.cljs$core$IFn$_invoke$arity$1(alyr);
var map__72158__$1 = ((((!((map__72158 == null)))?((((map__72158.cljs$lang$protocol_mask$partition0$ & (64))) || (map__72158.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__72158):map__72158);
var q_alpha = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72158__$1,cljs.core.cst$kw$q_DASH_alpha);
var q_discount = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__72158__$1,cljs.core.cst$kw$q_DASH_discount);
var Q_T = new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$var,"Q",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$sub,"t"], null)], null);
var Q_T_1 = new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$var$text_DASH_nowrap,"Q",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$sub,"t-1"], null)], null);
var R_T = new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$var$text_DASH_nowrap,"R",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$sub,"t"], null)], null);
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h4,"Q learning"], null),new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$table$table$table_DASH_condensed,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,R_T], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"reward"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,cljs.core.cst$kw$reward.cljs$core$IFn$_invoke$arity$2(qinfo,(0)).toFixed((2))], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,Q_T], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"goodness"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,cljs.core.cst$kw$Q_DASH_val.cljs$core$IFn$_invoke$arity$2(qinfo,(0)).toFixed((3))], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,Q_T_1], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"previous"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,cljs.core.cst$kw$Q_DASH_old.cljs$core$IFn$_invoke$arity$2(qinfo,(0)).toFixed((3))], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$var,"n"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"active synapses"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,cljs.core.cst$kw$perms.cljs$core$IFn$_invoke$arity$2(qinfo,(0))], null)], null)], null),new cljs.core.PersistentVector(null, 13, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_right,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$b,"adjustment: "], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$br], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$abbr,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$title,[cljs.core.str("learning rate, alpha")].join('')], null),q_alpha], null),"(",R_T," + ",new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$abbr,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$title,"discount factor"], null),q_discount], null),Q_T," - ",Q_T_1,") = ",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$mark,(function (){var G__72160 = "%+.3f";
var G__72161 = cljs.core.cst$kw$adj.cljs$core$IFn$_invoke$arity$2(qinfo,(0));
return goog.string.format(G__72160,G__72161);
})()], null)], null)], null);
});
org.numenta.sanity.demos.q_learning_1d.world_pane = (function org$numenta$sanity$demos$q_learning_1d$world_pane(){
var selected_htm = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.main.selection,cljs.core.cst$kw$org$numenta$sanity$demos$q_DASH_learning_DASH_1d_SLASH_fetch_DASH_selected_DASH_htm,((function (selected_htm){
return (function (_,___$1,___$2,p__72177){
var vec__72178 = p__72177;
var sel1 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__72178,(0),null);
var temp__4657__auto__ = cljs.core.get_in.cljs$core$IFn$_invoke$arity$2(sel1,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$step,cljs.core.cst$kw$snapshot_DASH_id], null));
if(cljs.core.truth_(temp__4657__auto__)){
var snapshot_id = temp__4657__auto__;
var out_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.into_journal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, ["get-model",snapshot_id,org.numenta.sanity.bridge.marshalling.channel.cljs$core$IFn$_invoke$arity$2(out_c,true)], null));

var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__72178,sel1,selected_htm){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__72178,sel1,selected_htm){
return (function (state_72183){
var state_val_72184 = (state_72183[(1)]);
if((state_val_72184 === (1))){
var state_72183__$1 = state_72183;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_72183__$1,(2),out_c);
} else {
if((state_val_72184 === (2))){
var inst_72180 = (state_72183[(2)]);
var inst_72181 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(selected_htm,inst_72180) : cljs.core.reset_BANG_.call(null,selected_htm,inst_72180));
var state_72183__$1 = state_72183;
return cljs.core.async.impl.ioc_helpers.return_chan(state_72183__$1,inst_72181);
} else {
return null;
}
}
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__72178,sel1,selected_htm))
;
return ((function (switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__72178,sel1,selected_htm){
return (function() {
var org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto____0 = (function (){
var statearr_72188 = [null,null,null,null,null,null,null];
(statearr_72188[(0)] = org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto__);

(statearr_72188[(1)] = (1));

return statearr_72188;
});
var org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto____1 = (function (state_72183){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_72183);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e72189){if((e72189 instanceof Object)){
var ex__37999__auto__ = e72189;
var statearr_72190_72192 = state_72183;
(statearr_72190_72192[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_72183);

return cljs.core.cst$kw$recur;
} else {
throw e72189;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__72193 = state_72183;
state_72183 = G__72193;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto__ = function(state_72183){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto____1.call(this,state_72183);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto____0;
org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$q_learning_1d$world_pane_$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__72178,sel1,selected_htm))
})();
var state__38111__auto__ = (function (){var statearr_72191 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_72191[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_72191;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,out_c,snapshot_id,temp__4657__auto__,vec__72178,sel1,selected_htm))
);

return c__38109__auto__;
} else {
return null;
}
});})(selected_htm))
);

return ((function (selected_htm){
return (function (){
var temp__4657__auto__ = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(selected_htm) : cljs.core.deref.call(null,selected_htm));
if(cljs.core.truth_(temp__4657__auto__)){
var htm = temp__4657__auto__;
var inval = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(htm);
var DELTA = goog.string.unescapeEntities("&Delta;");
var TIMES = goog.string.unescapeEntities("&times;");
return new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$muted,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Input on selected timestep."], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$muted,new cljs.core.PersistentVector(null, 8, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Reward ",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$var,"R"], null)," = ",DELTA,"y ",TIMES," 0.5"], null)], null),new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$table$table$table_DASH_condensed,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"x"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"position"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,cljs.core.cst$kw$x.cljs$core$IFn$_invoke$arity$1(inval)], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,[cljs.core.str(DELTA),cljs.core.str("x")].join('')], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"action"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,org.numenta.sanity.demos.q_learning_1d.signed_str(cljs.core.cst$kw$dx.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$prev_DASH_action.cljs$core$IFn$_invoke$arity$1(inval)))], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,[cljs.core.str(DELTA),cljs.core.str("y")].join('')], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"~reward"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,org.numenta.sanity.demos.q_learning_1d.signed_str(cljs.core.cst$kw$dy.cljs$core$IFn$_invoke$arity$1(inval))], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,[cljs.core.str(DELTA),cljs.core.str("x")].join(''),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$sub,"t+1"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"action"], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,org.numenta.sanity.demos.q_learning_1d.signed_str(cljs.core.cst$kw$dx.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$action.cljs$core$IFn$_invoke$arity$1(inval)))], null)], null)], null),org.numenta.sanity.demos.q_learning_1d.q_learning_sub_pane(htm),new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.helpers.resizing_canvas,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$width,"100%",cljs.core.cst$kw$height,"240px"], null)], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.selection], null),((function (inval,DELTA,TIMES,htm,temp__4657__auto__,selected_htm){
return (function (ctx){
var step = org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0();
var inval__$1 = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(step);
return org.numenta.sanity.demos.q_learning_1d.draw_world(ctx,inval__$1);
});})(inval,DELTA,TIMES,htm,temp__4657__auto__,selected_htm))
,null], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$b,"top: "], null),"Approx Q values for each position/action combination,\n            where green is positive and red is negative.\n            These are the last seen Q values including last adjustments."], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$b,"middle: "], null),"Current position on the objective function surface."], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$b,"bottom: "], null),"Frequencies of being at each position."], null)], null)], null);
} else {
return null;
}
});
;})(selected_htm))
});
org.numenta.sanity.demos.q_learning_1d.set_model_BANG_ = (function org$numenta$sanity$demos$q_learning_1d$set_model_BANG_(){
return org.numenta.sanity.helpers.with_ui_loading_message((function (){
var init_QMARK_ = ((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.q_learning_1d.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.q_learning_1d.model)) == null);
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,init_QMARK_){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,init_QMARK_){
return (function (state_72253){
var state_val_72254 = (state_72253[(1)]);
if((state_val_72254 === (1))){
var state_72253__$1 = state_72253;
if(init_QMARK_){
var statearr_72255_72272 = state_72253__$1;
(statearr_72255_72272[(1)] = (2));

} else {
var statearr_72256_72273 = state_72253__$1;
(statearr_72256_72273[(1)] = (3));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_72254 === (2))){
var state_72253__$1 = state_72253;
var statearr_72257_72274 = state_72253__$1;
(statearr_72257_72274[(2)] = null);

(statearr_72257_72274[(1)] = (4));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72254 === (3))){
var state_72253__$1 = state_72253;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_72253__$1,(5),org.numenta.sanity.demos.q_learning_1d.world_c);
} else {
if((state_val_72254 === (4))){
var inst_72238 = (state_72253[(2)]);
var inst_72239 = org.nfrac.comportex.demos.q_learning_1d.make_model();
var inst_72240 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.q_learning_1d.model,inst_72239) : cljs.core.reset_BANG_.call(null,org.numenta.sanity.demos.q_learning_1d.model,inst_72239));
var state_72253__$1 = (function (){var statearr_72258 = state_72253;
(statearr_72258[(7)] = inst_72238);

(statearr_72258[(8)] = inst_72240);

return statearr_72258;
})();
if(init_QMARK_){
var statearr_72259_72275 = state_72253__$1;
(statearr_72259_72275[(1)] = (6));

} else {
var statearr_72260_72276 = state_72253__$1;
(statearr_72260_72276[(1)] = (7));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_72254 === (5))){
var inst_72236 = (state_72253[(2)]);
var state_72253__$1 = state_72253;
var statearr_72261_72277 = state_72253__$1;
(statearr_72261_72277[(2)] = inst_72236);

(statearr_72261_72277[(1)] = (4));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72254 === (6))){
var inst_72242 = org.nfrac.comportex.demos.q_learning_1d.htm_step_with_action_selection(org.numenta.sanity.demos.q_learning_1d.world_c);
var inst_72243 = org.numenta.sanity.bridge.browser.init.cljs$core$IFn$_invoke$arity$5(org.numenta.sanity.demos.q_learning_1d.model,org.numenta.sanity.demos.q_learning_1d.world_c,org.numenta.sanity.main.into_journal,org.numenta.sanity.demos.q_learning_1d.into_sim,inst_72242);
var state_72253__$1 = state_72253;
var statearr_72262_72278 = state_72253__$1;
(statearr_72262_72278[(2)] = inst_72243);

(statearr_72262_72278[(1)] = (8));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72254 === (7))){
var inst_72245 = (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.q_learning_1d.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.q_learning_1d.model));
var inst_72246 = org.numenta.sanity.comportex.data.network_shape(inst_72245);
var inst_72247 = org.numenta.sanity.util.translate_network_shape(inst_72246);
var inst_72248 = (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.main.network_shape,inst_72247) : cljs.core.reset_BANG_.call(null,org.numenta.sanity.main.network_shape,inst_72247));
var state_72253__$1 = state_72253;
var statearr_72263_72279 = state_72253__$1;
(statearr_72263_72279[(2)] = inst_72248);

(statearr_72263_72279[(1)] = (8));


return cljs.core.cst$kw$recur;
} else {
if((state_val_72254 === (8))){
var inst_72250 = (state_72253[(2)]);
var inst_72251 = cljs.core.async.put_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.q_learning_1d.world_c,org.nfrac.comportex.demos.q_learning_1d.initial_inval);
var state_72253__$1 = (function (){var statearr_72264 = state_72253;
(statearr_72264[(9)] = inst_72250);

return statearr_72264;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_72253__$1,inst_72251);
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
});})(c__38109__auto__,init_QMARK_))
;
return ((function (switch__37995__auto__,c__38109__auto__,init_QMARK_){
return (function() {
var org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_72268 = [null,null,null,null,null,null,null,null,null,null];
(statearr_72268[(0)] = org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto__);

(statearr_72268[(1)] = (1));

return statearr_72268;
});
var org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto____1 = (function (state_72253){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_72253);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e72269){if((e72269 instanceof Object)){
var ex__37999__auto__ = e72269;
var statearr_72270_72280 = state_72253;
(statearr_72270_72280[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_72253);

return cljs.core.cst$kw$recur;
} else {
throw e72269;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__72281 = state_72253;
state_72253 = G__72281;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto__ = function(state_72253){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto____1.call(this,state_72253);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$q_learning_1d$set_model_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,init_QMARK_))
})();
var state__38111__auto__ = (function (){var statearr_72271 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_72271[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_72271;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,init_QMARK_))
);

return c__38109__auto__;
}));
});
org.numenta.sanity.demos.q_learning_1d.config_template = new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Number of regions:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$n_DASH_regions], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_offset_DASH_5$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.q_learning_1d.set_model_BANG_();

return e.preventDefault();
})], null),"Restart with new model"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_danger,"This resets all parameters."], null)], null)], null)], null);
org.numenta.sanity.demos.q_learning_1d.model_tab = (function org$numenta$sanity$demos$q_learning_1d$model_tab(){
return new cljs.core.PersistentVector(null, 14, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"Highly experimental attempt at integrating ",new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$a,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$href,"http://en.wikipedia.org/wiki/Q-learning"], null),"Q learning"], null)," (reinforcement learning)."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h4,"General approach"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"A Q value indicates the goodness of taking an action from some\n        state. We represent a Q value by the average permanence of\n        synapses activating the action from that state, minus the\n        initial permanence value."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"The action region columns are activated just like any other\n        region, but are then interpreted to produce an action."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"Adjustments to a Q value, based on reward and expected future\n        reward, are applied to the permanence of synapses which\n        directly activated the action (columns). This adjustment\n        applies in the action layer only, where it replaces the usual\n        learning of proximal synapses (spatial pooling)."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"Exploration arises from the usual boosting of neglected\n        columns, primarily in the action layer."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h4,"This example"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"The agent can move left or right on a reward surface. The\n        reward is proportional to the change in y value after\n        moving (dy)."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"The action layer columns are interpreted to produce an\n        action. 15 columns are allocated to each of the two directions\n        of movement, and the direction with most active columns is\n        used to move the agent."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"The input is the location of the agent via coordinate\n        encoder, plus the last movement as distal input."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"This example is continuous, not episodic. Success is\n        presumably indicated by the agent finding the optimum position\n        and staying there."], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"HTM model"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.bind_fields,org.numenta.sanity.demos.q_learning_1d.config_template,org.numenta.sanity.demos.q_learning_1d.config], null)], null);
});
org.numenta.sanity.demos.q_learning_1d.init = (function org$numenta$sanity$demos$q_learning_1d$init(){
reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,"Comportex",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.q_learning_1d.model_tab], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.q_learning_1d.world_pane], null),reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$model),org.numenta.sanity.demos.comportex_common.all_features,org.numenta.sanity.demos.q_learning_1d.into_sim], null),goog.dom.getElement("sanity-app"));

return org.numenta.sanity.demos.q_learning_1d.set_model_BANG_();
});
goog.exportSymbol('org.numenta.sanity.demos.q_learning_1d.init', org.numenta.sanity.demos.q_learning_1d.init);
