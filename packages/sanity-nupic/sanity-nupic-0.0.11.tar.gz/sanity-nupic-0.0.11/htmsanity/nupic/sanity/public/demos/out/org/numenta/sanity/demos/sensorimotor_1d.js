// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.demos.sensorimotor_1d');
goog.require('cljs.core');
goog.require('org.numenta.sanity.plots_canvas');
goog.require('goog.dom.forms');
goog.require('goog.dom');
goog.require('reagent.core');
goog.require('org.numenta.sanity.helpers');
goog.require('org.numenta.sanity.main');
goog.require('org.nfrac.comportex.demos.sensorimotor_1d');
goog.require('org.numenta.sanity.util');
goog.require('org.numenta.sanity.comportex.data');
goog.require('cljs.core.async');
goog.require('reagent_forms.core');
goog.require('org.nfrac.comportex.core');
goog.require('org.numenta.sanity.bridge.browser');
goog.require('org.numenta.sanity.demos.comportex_common');
goog.require('monet.canvas');
org.numenta.sanity.demos.sensorimotor_1d.config = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$n_DASH_regions,(1),cljs.core.cst$kw$field,cljs.core.cst$kw$abcdefghij,cljs.core.cst$kw$n_DASH_steps,(100),cljs.core.cst$kw$world_DASH_buffer_DASH_count,(0)], null));
org.numenta.sanity.demos.sensorimotor_1d.world_buffer = cljs.core.async.buffer((5000));
org.numenta.sanity.demos.sensorimotor_1d.world_c = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.sensorimotor_1d.world_buffer,cljs.core.map.cljs$core$IFn$_invoke$arity$1((function (p1__73185_SHARP_){
return cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(p1__73185_SHARP_,cljs.core.cst$kw$label,cljs.core.cst$kw$value.cljs$core$IFn$_invoke$arity$1(p1__73185_SHARP_));
})));
org.numenta.sanity.demos.sensorimotor_1d.into_sim = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$0();
org.numenta.sanity.demos.sensorimotor_1d.model = reagent.core.atom.cljs$core$IFn$_invoke$arity$1(null);
cljs.core.add_watch(org.numenta.sanity.demos.sensorimotor_1d.model,cljs.core.cst$kw$org$numenta$sanity$demos$sensorimotor_DASH_1d_SLASH_count_DASH_world_DASH_buffer,(function (_,___$1,___$2,___$3){
return cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.sensorimotor_1d.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.count(org.numenta.sanity.demos.sensorimotor_1d.world_buffer));
}));
org.numenta.sanity.demos.sensorimotor_1d.item_colors = cljs.core.zipmap(org.nfrac.comportex.demos.sensorimotor_1d.items,(function (){var iter__6925__auto__ = (function org$numenta$sanity$demos$sensorimotor_1d$iter__73186(s__73187){
return (new cljs.core.LazySeq(null,(function (){
var s__73187__$1 = s__73187;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__73187__$1);
if(temp__4657__auto__){
var s__73187__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__73187__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__73187__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__73189 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__73188 = (0);
while(true){
if((i__73188 < size__6924__auto__)){
var i = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__73188);
var hue = (i * (36));
var lig = ((cljs.core.even_QMARK_(i))?(70):(30));
cljs.core.chunk_append(b__73189,[cljs.core.str("hsl("),cljs.core.str(hue),cljs.core.str(",100%,"),cljs.core.str(lig),cljs.core.str("%)")].join(''));

var G__73192 = (i__73188 + (1));
i__73188 = G__73192;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__73189),org$numenta$sanity$demos$sensorimotor_1d$iter__73186(cljs.core.chunk_rest(s__73187__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__73189),null);
}
} else {
var i = cljs.core.first(s__73187__$2);
var hue = (i * (36));
var lig = ((cljs.core.even_QMARK_(i))?(70):(30));
return cljs.core.cons([cljs.core.str("hsl("),cljs.core.str(hue),cljs.core.str(",100%,"),cljs.core.str(lig),cljs.core.str("%)")].join(''),org$numenta$sanity$demos$sensorimotor_1d$iter__73186(cljs.core.rest(s__73187__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1((10)));
})());
org.numenta.sanity.demos.sensorimotor_1d.item_text_colors = cljs.core.zipmap(org.nfrac.comportex.demos.sensorimotor_1d.items,(function (){var iter__6925__auto__ = (function org$numenta$sanity$demos$sensorimotor_1d$iter__73193(s__73194){
return (new cljs.core.LazySeq(null,(function (){
var s__73194__$1 = s__73194;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__73194__$1);
if(temp__4657__auto__){
var s__73194__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__73194__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__73194__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__73196 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__73195 = (0);
while(true){
if((i__73195 < size__6924__auto__)){
var i = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__73195);
cljs.core.chunk_append(b__73196,((cljs.core.even_QMARK_(i))?"black":"white"));

var G__73199 = (i__73195 + (1));
i__73195 = G__73199;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__73196),org$numenta$sanity$demos$sensorimotor_1d$iter__73193(cljs.core.chunk_rest(s__73194__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__73196),null);
}
} else {
var i = cljs.core.first(s__73194__$2);
return cljs.core.cons(((cljs.core.even_QMARK_(i))?"black":"white"),org$numenta$sanity$demos$sensorimotor_1d$iter__73193(cljs.core.rest(s__73194__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.range.cljs$core$IFn$_invoke$arity$1((10)));
})());
org.numenta.sanity.demos.sensorimotor_1d.draw_eye = (function org$numenta$sanity$demos$sensorimotor_1d$draw_eye(ctx,p__73200){
var map__73203 = p__73200;
var map__73203__$1 = ((((!((map__73203 == null)))?((((map__73203.cljs$lang$protocol_mask$partition0$ & (64))) || (map__73203.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__73203):map__73203);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73203__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73203__$1,cljs.core.cst$kw$y);
var angle = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73203__$1,cljs.core.cst$kw$angle);
var radius = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73203__$1,cljs.core.cst$kw$radius);
monet.canvas.save(ctx);

var pi2_73205 = (Math.PI / (2));
monet.canvas.begin_path(ctx);

monet.canvas.arc(ctx,new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$x,x,cljs.core.cst$kw$y,y,cljs.core.cst$kw$r,radius,cljs.core.cst$kw$start_DASH_angle,(- pi2_73205),cljs.core.cst$kw$end_DASH_angle,pi2_73205,cljs.core.cst$kw$counter_DASH_clockwise_QMARK_,true], null));

monet.canvas.close_path(ctx);

monet.canvas.fill_style(ctx,"white");

monet.canvas.fill(ctx);

monet.canvas.stroke_style(ctx,"black");

monet.canvas.stroke(ctx);

monet.canvas.clip(ctx);

var pupil_x_73206 = (x + (radius * Math.cos(angle)));
var pupil_y_73207 = (y + (radius * Math.sin(angle)));
monet.canvas.circle(ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,pupil_x_73206,cljs.core.cst$kw$y,pupil_y_73207,cljs.core.cst$kw$r,cljs.core.quot(radius,(2))], null));

monet.canvas.fill_style(ctx,"rgb(128,128,255)");

monet.canvas.fill(ctx);

monet.canvas.circle(ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,pupil_x_73206,cljs.core.cst$kw$y,pupil_y_73207,cljs.core.cst$kw$r,cljs.core.quot(radius,(5))], null));

monet.canvas.fill_style(ctx,"black");

monet.canvas.fill(ctx);

return monet.canvas.restore(ctx);
});
org.numenta.sanity.demos.sensorimotor_1d.draw_world = (function org$numenta$sanity$demos$sensorimotor_1d$draw_world(ctx,in_value){
var map__73227 = in_value;
var map__73227__$1 = ((((!((map__73227 == null)))?((((map__73227.cljs$lang$protocol_mask$partition0$ & (64))) || (map__73227.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__73227):map__73227);
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73227__$1,cljs.core.cst$kw$field);
var position = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73227__$1,cljs.core.cst$kw$position);
var next_saccade = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73227__$1,cljs.core.cst$kw$next_DASH_saccade);
var item_w = (20);
var x_lim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),(1)], null);
var y_lim = new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),cljs.core.count(field)], null);
var width_px = ctx.canvas.width;
var height_px = ctx.canvas.height;
var plot_size = new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$w,width_px,cljs.core.cst$kw$h,(cljs.core.count(field) * item_w)], null);
var plot = org.numenta.sanity.plots_canvas.xy_plot(ctx,plot_size,x_lim,y_lim);
var x_scale = org.numenta.sanity.plots_canvas.scale_fn(x_lim,cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(plot_size));
var y_scale = org.numenta.sanity.plots_canvas.scale_fn(y_lim,cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(plot_size));
monet.canvas.clear_rect(ctx,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$w,width_px,cljs.core.cst$kw$h,height_px], null));

org.numenta.sanity.plots_canvas.frame_BANG_(plot);

monet.canvas.stroke_style(ctx,"black");

monet.canvas.font_style(ctx,"bold 14px monospace");

monet.canvas.text_baseline(ctx,cljs.core.cst$kw$middle);

var seq__73229_73246 = cljs.core.seq(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,field));
var chunk__73231_73247 = null;
var count__73232_73248 = (0);
var i__73233_73249 = (0);
while(true){
if((i__73233_73249 < count__73232_73248)){
var vec__73235_73250 = chunk__73231_73247.cljs$core$IIndexed$_nth$arity$2(null,i__73233_73249);
var y_73251 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73235_73250,(0),null);
var item_73252 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73235_73250,(1),null);
var rect_73253 = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(y_73251) : y_scale.call(null,y_73251)),cljs.core.cst$kw$w,item_w,cljs.core.cst$kw$h,(y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1((1)) : y_scale.call(null,(1)))], null);
var G__73236_73254 = ctx;
monet.canvas.fill_style(G__73236_73254,(org.numenta.sanity.demos.sensorimotor_1d.item_colors.cljs$core$IFn$_invoke$arity$1 ? org.numenta.sanity.demos.sensorimotor_1d.item_colors.cljs$core$IFn$_invoke$arity$1(item_73252) : org.numenta.sanity.demos.sensorimotor_1d.item_colors.call(null,item_73252)));

monet.canvas.fill_rect(G__73236_73254,rect_73253);

monet.canvas.stroke_rect(G__73236_73254,rect_73253);

monet.canvas.fill_style(G__73236_73254,(org.numenta.sanity.demos.sensorimotor_1d.item_text_colors.cljs$core$IFn$_invoke$arity$1 ? org.numenta.sanity.demos.sensorimotor_1d.item_text_colors.cljs$core$IFn$_invoke$arity$1(item_73252) : org.numenta.sanity.demos.sensorimotor_1d.item_text_colors.call(null,item_73252)));

monet.canvas.text(G__73236_73254,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,(5),cljs.core.cst$kw$y,(function (){var G__73237 = (y_73251 + 0.5);
return (y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(G__73237) : y_scale.call(null,G__73237));
})(),cljs.core.cst$kw$text,cljs.core.name(item_73252)], null));


var G__73255 = seq__73229_73246;
var G__73256 = chunk__73231_73247;
var G__73257 = count__73232_73248;
var G__73258 = (i__73233_73249 + (1));
seq__73229_73246 = G__73255;
chunk__73231_73247 = G__73256;
count__73232_73248 = G__73257;
i__73233_73249 = G__73258;
continue;
} else {
var temp__4657__auto___73259 = cljs.core.seq(seq__73229_73246);
if(temp__4657__auto___73259){
var seq__73229_73260__$1 = temp__4657__auto___73259;
if(cljs.core.chunked_seq_QMARK_(seq__73229_73260__$1)){
var c__6956__auto___73261 = cljs.core.chunk_first(seq__73229_73260__$1);
var G__73262 = cljs.core.chunk_rest(seq__73229_73260__$1);
var G__73263 = c__6956__auto___73261;
var G__73264 = cljs.core.count(c__6956__auto___73261);
var G__73265 = (0);
seq__73229_73246 = G__73262;
chunk__73231_73247 = G__73263;
count__73232_73248 = G__73264;
i__73233_73249 = G__73265;
continue;
} else {
var vec__73238_73266 = cljs.core.first(seq__73229_73260__$1);
var y_73267 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73238_73266,(0),null);
var item_73268 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__73238_73266,(1),null);
var rect_73269 = new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(y_73267) : y_scale.call(null,y_73267)),cljs.core.cst$kw$w,item_w,cljs.core.cst$kw$h,(y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1((1)) : y_scale.call(null,(1)))], null);
var G__73239_73270 = ctx;
monet.canvas.fill_style(G__73239_73270,(org.numenta.sanity.demos.sensorimotor_1d.item_colors.cljs$core$IFn$_invoke$arity$1 ? org.numenta.sanity.demos.sensorimotor_1d.item_colors.cljs$core$IFn$_invoke$arity$1(item_73268) : org.numenta.sanity.demos.sensorimotor_1d.item_colors.call(null,item_73268)));

monet.canvas.fill_rect(G__73239_73270,rect_73269);

monet.canvas.stroke_rect(G__73239_73270,rect_73269);

monet.canvas.fill_style(G__73239_73270,(org.numenta.sanity.demos.sensorimotor_1d.item_text_colors.cljs$core$IFn$_invoke$arity$1 ? org.numenta.sanity.demos.sensorimotor_1d.item_text_colors.cljs$core$IFn$_invoke$arity$1(item_73268) : org.numenta.sanity.demos.sensorimotor_1d.item_text_colors.call(null,item_73268)));

monet.canvas.text(G__73239_73270,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,(5),cljs.core.cst$kw$y,(function (){var G__73240 = (y_73267 + 0.5);
return (y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(G__73240) : y_scale.call(null,G__73240));
})(),cljs.core.cst$kw$text,cljs.core.name(item_73268)], null));


var G__73271 = cljs.core.next(seq__73229_73260__$1);
var G__73272 = null;
var G__73273 = (0);
var G__73274 = (0);
seq__73229_73246 = G__73271;
chunk__73231_73247 = G__73272;
count__73232_73248 = G__73273;
i__73233_73249 = G__73274;
continue;
}
} else {
}
}
break;
}

var focus_x = (10);
var focus_y = (function (){var G__73241 = (0.5 + position);
return (y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(G__73241) : y_scale.call(null,G__73241));
})();
var next_focus_y = (function (){var G__73242 = ((0.5 + position) + next_saccade);
return (y_scale.cljs$core$IFn$_invoke$arity$1 ? y_scale.cljs$core$IFn$_invoke$arity$1(G__73242) : y_scale.call(null,G__73242));
})();
var eye_x = cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(plot_size);
var eye_y = cljs.core.quot(cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(plot_size),(2));
var G__73243 = ctx;
monet.canvas.begin_path(G__73243);

monet.canvas.move_to(G__73243,eye_x,eye_y);

monet.canvas.line_to(G__73243,focus_x,next_focus_y);

monet.canvas.stroke_style(G__73243,"lightgrey");

monet.canvas.stroke(G__73243);

monet.canvas.begin_path(G__73243);

monet.canvas.move_to(G__73243,eye_x,eye_y);

monet.canvas.line_to(G__73243,focus_x,focus_y);

monet.canvas.stroke_style(G__73243,"black");

monet.canvas.stroke(G__73243);

org.numenta.sanity.demos.sensorimotor_1d.draw_eye(G__73243,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,eye_x,cljs.core.cst$kw$y,eye_y,cljs.core.cst$kw$angle,(function (){var G__73244 = (focus_y - eye_y);
var G__73245 = (focus_x - eye_x);
return Math.atan2(G__73244,G__73245);
})(),cljs.core.cst$kw$radius,(30)], null));

return G__73243;
});
org.numenta.sanity.demos.sensorimotor_1d.world_pane = (function org$numenta$sanity$demos$sensorimotor_1d$world_pane(){
var temp__4657__auto__ = org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0();
if(cljs.core.truth_(temp__4657__auto__)){
var step = temp__4657__auto__;
var in_value = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(step);
var map__73277 = in_value;
var map__73277__$1 = ((((!((map__73277 == null)))?((((map__73277.cljs$lang$protocol_mask$partition0$ & (64))) || (map__73277.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__73277):map__73277);
var field = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73277__$1,cljs.core.cst$kw$field);
var position = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73277__$1,cljs.core.cst$kw$position);
var next_saccade = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__73277__$1,cljs.core.cst$kw$next_DASH_saccade);
return new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$muted,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Input on selected timestep."], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$table$table,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"val"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,[cljs.core.str(cljs.core.get.cljs$core$IFn$_invoke$arity$2(field,position))].join('')], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$tr,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$th,"next"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$td,(((next_saccade < (0)))?"":"+"),next_saccade], null)], null)], null),new cljs.core.PersistentVector(null, 5, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.helpers.resizing_canvas,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$style,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$width,"100%",cljs.core.cst$kw$height,"300px"], null)], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.selection], null),((function (in_value,map__73277,map__73277__$1,field,position,next_saccade,step,temp__4657__auto__){
return (function (ctx){
var step__$1 = org.numenta.sanity.main.selected_step.cljs$core$IFn$_invoke$arity$0();
var in_value__$1 = cljs.core.cst$kw$input_DASH_value.cljs$core$IFn$_invoke$arity$1(step__$1);
return org.numenta.sanity.demos.sensorimotor_1d.draw_world(ctx,in_value__$1);
});})(in_value,map__73277,map__73277__$1,field,position,next_saccade,step,temp__4657__auto__))
,null], null)], null);
} else {
return null;
}
});
org.numenta.sanity.demos.sensorimotor_1d.seed_counter = reagent.core.atom.cljs$core$IFn$_invoke$arity$1((0));
org.numenta.sanity.demos.sensorimotor_1d.send_input_stream_BANG_ = (function org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG_(){
var field_key = cljs.core.cst$kw$field.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.sensorimotor_1d.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.sensorimotor_1d.config)));
var n_steps = cljs.core.cst$kw$n_DASH_steps.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.sensorimotor_1d.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.sensorimotor_1d.config)));
var field = (org.nfrac.comportex.demos.sensorimotor_1d.fields.cljs$core$IFn$_invoke$arity$1 ? org.nfrac.comportex.demos.sensorimotor_1d.fields.cljs$core$IFn$_invoke$arity$1(field_key) : org.nfrac.comportex.demos.sensorimotor_1d.fields.call(null,field_key));
var c__38109__auto__ = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto__,field_key,n_steps,field){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto__,field_key,n_steps,field){
return (function (state_73309){
var state_val_73310 = (state_73309[(1)]);
if((state_val_73310 === (1))){
var inst_73299 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$2(org.numenta.sanity.demos.sensorimotor_1d.seed_counter,cljs.core.inc);
var inst_73300 = org.nfrac.comportex.demos.sensorimotor_1d.initial_world(field,inst_73299);
var inst_73301 = org.nfrac.comportex.demos.sensorimotor_1d.input_seq(inst_73300);
var inst_73302 = cljs.core.take.cljs$core$IFn$_invoke$arity$2(n_steps,inst_73301);
var inst_73303 = cljs.core.async.onto_chan.cljs$core$IFn$_invoke$arity$3(org.numenta.sanity.demos.sensorimotor_1d.world_c,inst_73302,false);
var state_73309__$1 = state_73309;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73309__$1,(2),inst_73303);
} else {
if((state_val_73310 === (2))){
var inst_73305 = (state_73309[(2)]);
var inst_73306 = cljs.core.count(org.numenta.sanity.demos.sensorimotor_1d.world_buffer);
var inst_73307 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.sensorimotor_1d.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,inst_73306);
var state_73309__$1 = (function (){var statearr_73311 = state_73309;
(statearr_73311[(7)] = inst_73305);

return statearr_73311;
})();
return cljs.core.async.impl.ioc_helpers.return_chan(state_73309__$1,inst_73307);
} else {
return null;
}
}
});})(c__38109__auto__,field_key,n_steps,field))
;
return ((function (switch__37995__auto__,c__38109__auto__,field_key,n_steps,field){
return (function() {
var org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto____0 = (function (){
var statearr_73315 = [null,null,null,null,null,null,null,null];
(statearr_73315[(0)] = org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto__);

(statearr_73315[(1)] = (1));

return statearr_73315;
});
var org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto____1 = (function (state_73309){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_73309);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e73316){if((e73316 instanceof Object)){
var ex__37999__auto__ = e73316;
var statearr_73317_73319 = state_73309;
(statearr_73317_73319[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_73309);

return cljs.core.cst$kw$recur;
} else {
throw e73316;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__73320 = state_73309;
state_73309 = G__73320;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto__ = function(state_73309){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto____1.call(this,state_73309);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto____0;
org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto____1;
return org$numenta$sanity$demos$sensorimotor_1d$send_input_stream_BANG__$_state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto__,field_key,n_steps,field))
})();
var state__38111__auto__ = (function (){var statearr_73318 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_73318[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto__);

return statearr_73318;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto__,field_key,n_steps,field))
);

return c__38109__auto__;
});
org.numenta.sanity.demos.sensorimotor_1d.set_model_BANG_ = (function org$numenta$sanity$demos$sensorimotor_1d$set_model_BANG_(){
return org.numenta.sanity.helpers.with_ui_loading_message((function (){
var init_QMARK_ = ((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.sensorimotor_1d.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.sensorimotor_1d.model)) == null);
var G__73325_73329 = org.numenta.sanity.demos.sensorimotor_1d.model;
var G__73326_73330 = org.nfrac.comportex.demos.sensorimotor_1d.n_region_model.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$n_DASH_regions.cljs$core$IFn$_invoke$arity$1((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.sensorimotor_1d.config) : cljs.core.deref.call(null,org.numenta.sanity.demos.sensorimotor_1d.config))));
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__73325_73329,G__73326_73330) : cljs.core.reset_BANG_.call(null,G__73325_73329,G__73326_73330));

if(init_QMARK_){
return org.numenta.sanity.bridge.browser.init.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.sensorimotor_1d.model,org.numenta.sanity.demos.sensorimotor_1d.world_c,org.numenta.sanity.main.into_journal,org.numenta.sanity.demos.sensorimotor_1d.into_sim);
} else {
var G__73327 = org.numenta.sanity.main.network_shape;
var G__73328 = org.numenta.sanity.util.translate_network_shape(org.numenta.sanity.comportex.data.network_shape((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(org.numenta.sanity.demos.sensorimotor_1d.model) : cljs.core.deref.call(null,org.numenta.sanity.demos.sensorimotor_1d.model))));
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__73327,G__73328) : cljs.core.reset_BANG_.call(null,G__73327,G__73328));
}
}));
});
org.numenta.sanity.demos.sensorimotor_1d.config_template = new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"Input ",new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$small,"Sensorimotor sequences"], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_info,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$field,cljs.core.cst$kw$label,cljs.core.cst$kw$id,cljs.core.cst$kw$world_DASH_buffer_DASH_count,cljs.core.cst$kw$postamble," queued input values."], null)], null)," ",new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$span,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$container,cljs.core.cst$kw$visible_QMARK_,(function (p1__73331_SHARP_){
return (cljs.core.cst$kw$world_DASH_buffer_DASH_count.cljs$core$IFn$_invoke$arity$1(p1__73331_SHARP_) > (0));
})], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_warning$btn_DASH_xs,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
var c__38109__auto___73378 = cljs.core.async.chan.cljs$core$IFn$_invoke$arity$1((1));
cljs.core.async.impl.dispatch.run(((function (c__38109__auto___73378){
return (function (){
var f__38110__auto__ = (function (){var switch__37995__auto__ = ((function (c__38109__auto___73378){
return (function (state_73351){
var state_val_73352 = (state_73351[(1)]);
if((state_val_73352 === (7))){
var inst_73337 = (state_73351[(2)]);
var state_73351__$1 = state_73351;
var statearr_73353_73379 = state_73351__$1;
(statearr_73353_73379[(2)] = inst_73337);

(statearr_73353_73379[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73352 === (1))){
var state_73351__$1 = state_73351;
var statearr_73354_73380 = state_73351__$1;
(statearr_73354_73380[(2)] = null);

(statearr_73354_73380[(1)] = (2));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73352 === (4))){
var state_73351__$1 = state_73351;
return cljs.core.async.impl.ioc_helpers.take_BANG_(state_73351__$1,(7),org.numenta.sanity.demos.sensorimotor_1d.world_c);
} else {
if((state_val_73352 === (6))){
var inst_73340 = (state_73351[(2)]);
var state_73351__$1 = state_73351;
if(cljs.core.truth_(inst_73340)){
var statearr_73355_73381 = state_73351__$1;
(statearr_73355_73381[(1)] = (8));

} else {
var statearr_73356_73382 = state_73351__$1;
(statearr_73356_73382[(1)] = (9));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_73352 === (3))){
var inst_73349 = (state_73351[(2)]);
var state_73351__$1 = state_73351;
return cljs.core.async.impl.ioc_helpers.return_chan(state_73351__$1,inst_73349);
} else {
if((state_val_73352 === (2))){
var inst_73334 = (state_73351[(7)]);
var inst_73333 = cljs.core.count(org.numenta.sanity.demos.sensorimotor_1d.world_buffer);
var inst_73334__$1 = (inst_73333 > (0));
var state_73351__$1 = (function (){var statearr_73357 = state_73351;
(statearr_73357[(7)] = inst_73334__$1);

return statearr_73357;
})();
if(cljs.core.truth_(inst_73334__$1)){
var statearr_73358_73383 = state_73351__$1;
(statearr_73358_73383[(1)] = (4));

} else {
var statearr_73359_73384 = state_73351__$1;
(statearr_73359_73384[(1)] = (5));

}

return cljs.core.cst$kw$recur;
} else {
if((state_val_73352 === (9))){
var state_73351__$1 = state_73351;
var statearr_73360_73385 = state_73351__$1;
(statearr_73360_73385[(2)] = null);

(statearr_73360_73385[(1)] = (10));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73352 === (5))){
var inst_73334 = (state_73351[(7)]);
var state_73351__$1 = state_73351;
var statearr_73361_73386 = state_73351__$1;
(statearr_73361_73386[(2)] = inst_73334);

(statearr_73361_73386[(1)] = (6));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73352 === (10))){
var inst_73347 = (state_73351[(2)]);
var state_73351__$1 = state_73351;
var statearr_73362_73387 = state_73351__$1;
(statearr_73362_73387[(2)] = inst_73347);

(statearr_73362_73387[(1)] = (3));


return cljs.core.cst$kw$recur;
} else {
if((state_val_73352 === (8))){
var inst_73342 = cljs.core.count(org.numenta.sanity.demos.sensorimotor_1d.world_buffer);
var inst_73343 = cljs.core.swap_BANG_.cljs$core$IFn$_invoke$arity$4(org.numenta.sanity.demos.sensorimotor_1d.config,cljs.core.assoc,cljs.core.cst$kw$world_DASH_buffer_DASH_count,inst_73342);
var state_73351__$1 = (function (){var statearr_73363 = state_73351;
(statearr_73363[(8)] = inst_73343);

return statearr_73363;
})();
var statearr_73364_73388 = state_73351__$1;
(statearr_73364_73388[(2)] = null);

(statearr_73364_73388[(1)] = (2));


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
});})(c__38109__auto___73378))
;
return ((function (switch__37995__auto__,c__38109__auto___73378){
return (function() {
var org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto__ = null;
var org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto____0 = (function (){
var statearr_73368 = [null,null,null,null,null,null,null,null,null];
(statearr_73368[(0)] = org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto__);

(statearr_73368[(1)] = (1));

return statearr_73368;
});
var org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto____1 = (function (state_73351){
while(true){
var ret_value__37997__auto__ = (function (){try{while(true){
var result__37998__auto__ = switch__37995__auto__(state_73351);
if(cljs.core.keyword_identical_QMARK_(result__37998__auto__,cljs.core.cst$kw$recur)){
continue;
} else {
return result__37998__auto__;
}
break;
}
}catch (e73369){if((e73369 instanceof Object)){
var ex__37999__auto__ = e73369;
var statearr_73370_73389 = state_73351;
(statearr_73370_73389[(5)] = ex__37999__auto__);


cljs.core.async.impl.ioc_helpers.process_exception(state_73351);

return cljs.core.cst$kw$recur;
} else {
throw e73369;

}
}})();
if(cljs.core.keyword_identical_QMARK_(ret_value__37997__auto__,cljs.core.cst$kw$recur)){
var G__73390 = state_73351;
state_73351 = G__73390;
continue;
} else {
return ret_value__37997__auto__;
}
break;
}
});
org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto__ = function(state_73351){
switch(arguments.length){
case 0:
return org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto____0.call(this);
case 1:
return org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto____1.call(this,state_73351);
}
throw(new Error('Invalid arity: ' + arguments.length));
};
org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$0 = org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto____0;
org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto__.cljs$core$IFn$_invoke$arity$1 = org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto____1;
return org$numenta$sanity$demos$sensorimotor_1d$state_machine__37996__auto__;
})()
;})(switch__37995__auto__,c__38109__auto___73378))
})();
var state__38111__auto__ = (function (){var statearr_73371 = (f__38110__auto__.cljs$core$IFn$_invoke$arity$0 ? f__38110__auto__.cljs$core$IFn$_invoke$arity$0() : f__38110__auto__.call(null));
(statearr_73371[cljs.core.async.impl.ioc_helpers.USER_START_IDX] = c__38109__auto___73378);

return statearr_73371;
})();
return cljs.core.async.impl.ioc_helpers.run_state_machine_wrapped(state__38111__auto__);
});})(c__38109__auto___73378))
);


return e.preventDefault();
})], null),"Clear"], null)], null)], null),new cljs.core.PersistentVector(null, 4, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Field of values (a world):"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$select$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$list,cljs.core.cst$kw$id,cljs.core.cst$kw$field], null),(function (){var iter__6925__auto__ = (function org$numenta$sanity$demos$sensorimotor_1d$iter__73372(s__73373){
return (new cljs.core.LazySeq(null,(function (){
var s__73373__$1 = s__73373;
while(true){
var temp__4657__auto__ = cljs.core.seq(s__73373__$1);
if(temp__4657__auto__){
var s__73373__$2 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(s__73373__$2)){
var c__6923__auto__ = cljs.core.chunk_first(s__73373__$2);
var size__6924__auto__ = cljs.core.count(c__6923__auto__);
var b__73375 = cljs.core.chunk_buffer(size__6924__auto__);
if((function (){var i__73374 = (0);
while(true){
if((i__73374 < size__6924__auto__)){
var k = cljs.core._nth.cljs$core$IFn$_invoke$arity$2(c__6923__auto__,i__73374);
cljs.core.chunk_append(b__73375,cljs.core.with_meta(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$option,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,k], null),cljs.core.name(k)], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,k], null)));

var G__73391 = (i__73374 + (1));
i__73374 = G__73391;
continue;
} else {
return true;
}
break;
}
})()){
return cljs.core.chunk_cons(cljs.core.chunk(b__73375),org$numenta$sanity$demos$sensorimotor_1d$iter__73372(cljs.core.chunk_rest(s__73373__$2)));
} else {
return cljs.core.chunk_cons(cljs.core.chunk(b__73375),null);
}
} else {
var k = cljs.core.first(s__73373__$2);
return cljs.core.cons(cljs.core.with_meta(new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$option,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,k], null),cljs.core.name(k)], null),new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$key,k], null)),org$numenta$sanity$demos$sensorimotor_1d$iter__73372(cljs.core.rest(s__73373__$2)));
}
} else {
return null;
}
break;
}
}),null,null));
});
return iter__6925__auto__(cljs.core.keys(org.nfrac.comportex.demos.sensorimotor_1d.fields));
})()], null)], null)], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Number of steps:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$n_DASH_steps], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_offset_DASH_5$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_primary,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.sensorimotor_1d.send_input_stream_BANG_();

return e.preventDefault();
})], null),"Send input stream"], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$h3,"HTM model"], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_horizontal,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$label$col_DASH_sm_DASH_5,"Number of regions:"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$input$form_DASH_control,new cljs.core.PersistentArrayMap(null, 2, [cljs.core.cst$kw$field,cljs.core.cst$kw$numeric,cljs.core.cst$kw$id,cljs.core.cst$kw$n_DASH_regions], null)], null)], null)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$form_DASH_group,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div$col_DASH_sm_DASH_offset_DASH_5$col_DASH_sm_DASH_7,new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$button$btn$btn_DASH_default,new cljs.core.PersistentArrayMap(null, 1, [cljs.core.cst$kw$on_DASH_click,(function (e){
org.numenta.sanity.demos.sensorimotor_1d.set_model_BANG_();

return e.preventDefault();
})], null),"Restart with new model"], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p$text_DASH_danger,"This resets all parameters."], null)], null)], null)], null)], null);
org.numenta.sanity.demos.sensorimotor_1d.model_tab = (function org$numenta$sanity$demos$sensorimotor_1d$model_tab(){
return new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$div,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$p,"A simple example of sensorimotor input in 1D."], null),new cljs.core.PersistentVector(null, 3, 5, cljs.core.PersistentVector.EMPTY_NODE, [reagent_forms.core.bind_fields,org.numenta.sanity.demos.sensorimotor_1d.config_template,org.numenta.sanity.demos.sensorimotor_1d.config], null)], null);
});
org.numenta.sanity.demos.sensorimotor_1d.init = (function org$numenta$sanity$demos$sensorimotor_1d$init(){
reagent.core.render.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 7, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.main.sanity_app,"Comportex",new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.sensorimotor_1d.model_tab], null),new cljs.core.PersistentVector(null, 1, 5, cljs.core.PersistentVector.EMPTY_NODE, [org.numenta.sanity.demos.sensorimotor_1d.world_pane], null),reagent.core.atom.cljs$core$IFn$_invoke$arity$1(cljs.core.cst$kw$model),org.numenta.sanity.demos.comportex_common.all_features,org.numenta.sanity.demos.sensorimotor_1d.into_sim], null),goog.dom.getElement("sanity-app"));

org.numenta.sanity.demos.sensorimotor_1d.send_input_stream_BANG_();

return org.numenta.sanity.demos.sensorimotor_1d.set_model_BANG_();
});
goog.exportSymbol('org.numenta.sanity.demos.sensorimotor_1d.init', org.numenta.sanity.demos.sensorimotor_1d.init);
