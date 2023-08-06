// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('org.numenta.sanity.plots_canvas');
goog.require('cljs.core');
goog.require('monet.canvas');
org.numenta.sanity.plots_canvas.indexed = (function org$numenta$sanity$plots_canvas$indexed(ys){
return cljs.core.vec(cljs.core.map_indexed.cljs$core$IFn$_invoke$arity$2(cljs.core.vector,ys));
});

/**
 * @interface
 */
org.numenta.sanity.plots_canvas.PPlot = function(){};

org.numenta.sanity.plots_canvas.bg_BANG_ = (function org$numenta$sanity$plots_canvas$bg_BANG_(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$bg_BANG_$arity$1 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$bg_BANG_$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.bg_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.bg_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PPlot.bg!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.frame_BANG_ = (function org$numenta$sanity$plots_canvas$frame_BANG_(this$){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$frame_BANG_$arity$1 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$frame_BANG_$arity$1(this$);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.frame_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto__.call(null,this$));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.frame_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$1(this$) : m__6809__auto____$1.call(null,this$));
} else {
throw cljs.core.missing_protocol("PPlot.frame!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.grid_BANG_ = (function org$numenta$sanity$plots_canvas$grid_BANG_(this$,opts){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$grid_BANG_$arity$2 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$grid_BANG_$arity$2(this$,opts);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.grid_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,opts) : m__6809__auto__.call(null,this$,opts));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.grid_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,opts) : m__6809__auto____$1.call(null,this$,opts));
} else {
throw cljs.core.missing_protocol("PPlot.grid!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.point_BANG_ = (function org$numenta$sanity$plots_canvas$point_BANG_(this$,x,y,radius_px){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$point_BANG_$arity$4 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$point_BANG_$arity$4(this$,x,y,radius_px);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.point_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$4(this$,x,y,radius_px) : m__6809__auto__.call(null,this$,x,y,radius_px));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.point_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4(this$,x,y,radius_px) : m__6809__auto____$1.call(null,this$,x,y,radius_px));
} else {
throw cljs.core.missing_protocol("PPlot.point!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.rect_BANG_ = (function org$numenta$sanity$plots_canvas$rect_BANG_(this$,x,y,w,h){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$rect_BANG_$arity$5 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$rect_BANG_$arity$5(this$,x,y,w,h);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.rect_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$5 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$5(this$,x,y,w,h) : m__6809__auto__.call(null,this$,x,y,w,h));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.rect_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$5 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$5(this$,x,y,w,h) : m__6809__auto____$1.call(null,this$,x,y,w,h));
} else {
throw cljs.core.missing_protocol("PPlot.rect!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.line_BANG_ = (function org$numenta$sanity$plots_canvas$line_BANG_(this$,xys){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$line_BANG_$arity$2 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$line_BANG_$arity$2(this$,xys);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.line_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$2(this$,xys) : m__6809__auto__.call(null,this$,xys));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.line_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$2(this$,xys) : m__6809__auto____$1.call(null,this$,xys));
} else {
throw cljs.core.missing_protocol("PPlot.line!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.text_BANG_ = (function org$numenta$sanity$plots_canvas$text_BANG_(this$,x,y,txt){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$text_BANG_$arity$4 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$text_BANG_$arity$4(this$,x,y,txt);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.text_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$4(this$,x,y,txt) : m__6809__auto__.call(null,this$,x,y,txt));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.text_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4(this$,x,y,txt) : m__6809__auto____$1.call(null,this$,x,y,txt));
} else {
throw cljs.core.missing_protocol("PPlot.text!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.texts_BANG_ = (function org$numenta$sanity$plots_canvas$texts_BANG_(this$,x,y,txts,line_height){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$texts_BANG_$arity$5 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$texts_BANG_$arity$5(this$,x,y,txts,line_height);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.texts_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$5 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$5(this$,x,y,txts,line_height) : m__6809__auto__.call(null,this$,x,y,txts,line_height));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.texts_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$5 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$5(this$,x,y,txts,line_height) : m__6809__auto____$1.call(null,this$,x,y,txts,line_height));
} else {
throw cljs.core.missing_protocol("PPlot.texts!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.text_rotated_BANG_ = (function org$numenta$sanity$plots_canvas$text_rotated_BANG_(this$,x,y,txt){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$text_rotated_BANG_$arity$4 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$text_rotated_BANG_$arity$4(this$,x,y,txt);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.text_rotated_BANG_[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$4(this$,x,y,txt) : m__6809__auto__.call(null,this$,x,y,txt));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.text_rotated_BANG_["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$4(this$,x,y,txt) : m__6809__auto____$1.call(null,this$,x,y,txt));
} else {
throw cljs.core.missing_protocol("PPlot.text-rotated!",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.__GT_px = (function org$numenta$sanity$plots_canvas$__GT_px(this$,x,y){
if((!((this$ == null))) && (!((this$.org$numenta$sanity$plots_canvas$PPlot$__GT_px$arity$3 == null)))){
return this$.org$numenta$sanity$plots_canvas$PPlot$__GT_px$arity$3(this$,x,y);
} else {
var x__6808__auto__ = (((this$ == null))?null:this$);
var m__6809__auto__ = (org.numenta.sanity.plots_canvas.__GT_px[goog.typeOf(x__6808__auto__)]);
if(!((m__6809__auto__ == null))){
return (m__6809__auto__.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto__.cljs$core$IFn$_invoke$arity$3(this$,x,y) : m__6809__auto__.call(null,this$,x,y));
} else {
var m__6809__auto____$1 = (org.numenta.sanity.plots_canvas.__GT_px["_"]);
if(!((m__6809__auto____$1 == null))){
return (m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3 ? m__6809__auto____$1.cljs$core$IFn$_invoke$arity$3(this$,x,y) : m__6809__auto____$1.call(null,this$,x,y));
} else {
throw cljs.core.missing_protocol("PPlot.->px",this$);
}
}
}
});

org.numenta.sanity.plots_canvas.draw_grid = (function org$numenta$sanity$plots_canvas$draw_grid(ctx,p__59415,p__59416,xs,ys){
var vec__59427 = p__59415;
var x_lo = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59427,(0),null);
var x_hi = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59427,(1),null);
var vec__59428 = p__59416;
var y_lo = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59428,(0),null);
var y_hi = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59428,(1),null);
monet.canvas.begin_path(ctx);

var seq__59429_59437 = cljs.core.seq(xs);
var chunk__59430_59438 = null;
var count__59431_59439 = (0);
var i__59432_59440 = (0);
while(true){
if((i__59432_59440 < count__59431_59439)){
var x_59441 = chunk__59430_59438.cljs$core$IIndexed$_nth$arity$2(null,i__59432_59440);
monet.canvas.move_to(ctx,x_59441,y_lo);

monet.canvas.line_to(ctx,x_59441,y_hi);

var G__59442 = seq__59429_59437;
var G__59443 = chunk__59430_59438;
var G__59444 = count__59431_59439;
var G__59445 = (i__59432_59440 + (1));
seq__59429_59437 = G__59442;
chunk__59430_59438 = G__59443;
count__59431_59439 = G__59444;
i__59432_59440 = G__59445;
continue;
} else {
var temp__4657__auto___59446 = cljs.core.seq(seq__59429_59437);
if(temp__4657__auto___59446){
var seq__59429_59447__$1 = temp__4657__auto___59446;
if(cljs.core.chunked_seq_QMARK_(seq__59429_59447__$1)){
var c__6956__auto___59448 = cljs.core.chunk_first(seq__59429_59447__$1);
var G__59449 = cljs.core.chunk_rest(seq__59429_59447__$1);
var G__59450 = c__6956__auto___59448;
var G__59451 = cljs.core.count(c__6956__auto___59448);
var G__59452 = (0);
seq__59429_59437 = G__59449;
chunk__59430_59438 = G__59450;
count__59431_59439 = G__59451;
i__59432_59440 = G__59452;
continue;
} else {
var x_59453 = cljs.core.first(seq__59429_59447__$1);
monet.canvas.move_to(ctx,x_59453,y_lo);

monet.canvas.line_to(ctx,x_59453,y_hi);

var G__59454 = cljs.core.next(seq__59429_59447__$1);
var G__59455 = null;
var G__59456 = (0);
var G__59457 = (0);
seq__59429_59437 = G__59454;
chunk__59430_59438 = G__59455;
count__59431_59439 = G__59456;
i__59432_59440 = G__59457;
continue;
}
} else {
}
}
break;
}

var seq__59433_59458 = cljs.core.seq(ys);
var chunk__59434_59459 = null;
var count__59435_59460 = (0);
var i__59436_59461 = (0);
while(true){
if((i__59436_59461 < count__59435_59460)){
var y_59462 = chunk__59434_59459.cljs$core$IIndexed$_nth$arity$2(null,i__59436_59461);
monet.canvas.move_to(ctx,x_lo,y_59462);

monet.canvas.line_to(ctx,x_hi,y_59462);

var G__59463 = seq__59433_59458;
var G__59464 = chunk__59434_59459;
var G__59465 = count__59435_59460;
var G__59466 = (i__59436_59461 + (1));
seq__59433_59458 = G__59463;
chunk__59434_59459 = G__59464;
count__59435_59460 = G__59465;
i__59436_59461 = G__59466;
continue;
} else {
var temp__4657__auto___59467 = cljs.core.seq(seq__59433_59458);
if(temp__4657__auto___59467){
var seq__59433_59468__$1 = temp__4657__auto___59467;
if(cljs.core.chunked_seq_QMARK_(seq__59433_59468__$1)){
var c__6956__auto___59469 = cljs.core.chunk_first(seq__59433_59468__$1);
var G__59470 = cljs.core.chunk_rest(seq__59433_59468__$1);
var G__59471 = c__6956__auto___59469;
var G__59472 = cljs.core.count(c__6956__auto___59469);
var G__59473 = (0);
seq__59433_59458 = G__59470;
chunk__59434_59459 = G__59471;
count__59435_59460 = G__59472;
i__59436_59461 = G__59473;
continue;
} else {
var y_59474 = cljs.core.first(seq__59433_59468__$1);
monet.canvas.move_to(ctx,x_lo,y_59474);

monet.canvas.line_to(ctx,x_hi,y_59474);

var G__59475 = cljs.core.next(seq__59433_59468__$1);
var G__59476 = null;
var G__59477 = (0);
var G__59478 = (0);
seq__59433_59458 = G__59475;
chunk__59434_59459 = G__59476;
count__59435_59460 = G__59477;
i__59436_59461 = G__59478;
continue;
}
} else {
}
}
break;
}

return monet.canvas.stroke(ctx);
});
org.numenta.sanity.plots_canvas.scale_fn = (function org$numenta$sanity$plots_canvas$scale_fn(p__59479,size_px){
var vec__59481 = p__59479;
var lo = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59481,(0),null);
var hi = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59481,(1),null);
return ((function (vec__59481,lo,hi){
return (function (x){
return ((x - lo) * (size_px / (hi - lo)));
});
;})(vec__59481,lo,hi))
});
org.numenta.sanity.plots_canvas.text_rotated = (function org$numenta$sanity$plots_canvas$text_rotated(ctx,p__59482){
var map__59485 = p__59482;
var map__59485__$1 = ((((!((map__59485 == null)))?((((map__59485.cljs$lang$protocol_mask$partition0$ & (64))) || (map__59485.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__59485):map__59485);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__59485__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__59485__$1,cljs.core.cst$kw$y);
var text = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__59485__$1,cljs.core.cst$kw$text);
monet.canvas.save(ctx);

monet.canvas.translate(ctx,x,y);

monet.canvas.rotate(ctx,(Math.PI / (2)));

monet.canvas.text(ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$text,text], null));

return monet.canvas.restore(ctx);
});

/**
* @constructor
 * @implements {cljs.core.IRecord}
 * @implements {cljs.core.IEquiv}
 * @implements {cljs.core.IHash}
 * @implements {cljs.core.ICollection}
 * @implements {cljs.core.ICounted}
 * @implements {cljs.core.ISeqable}
 * @implements {cljs.core.IMeta}
 * @implements {cljs.core.ICloneable}
 * @implements {org.numenta.sanity.plots_canvas.PPlot}
 * @implements {cljs.core.IPrintWithWriter}
 * @implements {cljs.core.IIterable}
 * @implements {cljs.core.IWithMeta}
 * @implements {cljs.core.IAssociative}
 * @implements {cljs.core.IMap}
 * @implements {cljs.core.ILookup}
*/
org.numenta.sanity.plots_canvas.XYPlot = (function (ctx,plot_size,x_lim,y_lim,x_scale,y_scale,__meta,__extmap,__hash){
this.ctx = ctx;
this.plot_size = plot_size;
this.x_lim = x_lim;
this.y_lim = y_lim;
this.x_scale = x_scale;
this.y_scale = y_scale;
this.__meta = __meta;
this.__extmap = __extmap;
this.__hash = __hash;
this.cljs$lang$protocol_mask$partition0$ = 2229667594;
this.cljs$lang$protocol_mask$partition1$ = 8192;
})
org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$ILookup$_lookup$arity$2 = (function (this__6767__auto__,k__6768__auto__){
var self__ = this;
var this__6767__auto____$1 = this;
return cljs.core._lookup.cljs$core$IFn$_invoke$arity$3(this__6767__auto____$1,k__6768__auto__,null);
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$ILookup$_lookup$arity$3 = (function (this__6769__auto__,k59488,else__6770__auto__){
var self__ = this;
var this__6769__auto____$1 = this;
var G__59490 = (((k59488 instanceof cljs.core.Keyword))?k59488.fqn:null);
switch (G__59490) {
case "ctx":
return self__.ctx;

break;
case "plot-size":
return self__.plot_size;

break;
case "x-lim":
return self__.x_lim;

break;
case "y-lim":
return self__.y_lim;

break;
case "x-scale":
return self__.x_scale;

break;
case "y-scale":
return self__.y_scale;

break;
default:
return cljs.core.get.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k59488,else__6770__auto__);

}
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IPrintWithWriter$_pr_writer$arity$3 = (function (this__6781__auto__,writer__6782__auto__,opts__6783__auto__){
var self__ = this;
var this__6781__auto____$1 = this;
var pr_pair__6784__auto__ = ((function (this__6781__auto____$1){
return (function (keyval__6785__auto__){
return cljs.core.pr_sequential_writer(writer__6782__auto__,cljs.core.pr_writer,""," ","",opts__6783__auto__,keyval__6785__auto__);
});})(this__6781__auto____$1))
;
return cljs.core.pr_sequential_writer(writer__6782__auto__,pr_pair__6784__auto__,"#org.numenta.sanity.plots-canvas.XYPlot{",", ","}",opts__6783__auto__,cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ctx,self__.ctx],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$plot_DASH_size,self__.plot_size],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$x_DASH_lim,self__.x_lim],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$y_DASH_lim,self__.y_lim],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$x_DASH_scale,self__.x_scale],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$y_DASH_scale,self__.y_scale],null))], null),self__.__extmap));
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IIterable$ = true;

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IIterable$_iterator$arity$1 = (function (G__59487){
var self__ = this;
var G__59487__$1 = this;
return (new cljs.core.RecordIter((0),G__59487__$1,6,new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$kw$ctx,cljs.core.cst$kw$plot_DASH_size,cljs.core.cst$kw$x_DASH_lim,cljs.core.cst$kw$y_DASH_lim,cljs.core.cst$kw$x_DASH_scale,cljs.core.cst$kw$y_DASH_scale], null),cljs.core._iterator(self__.__extmap)));
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IMeta$_meta$arity$1 = (function (this__6765__auto__){
var self__ = this;
var this__6765__auto____$1 = this;
return self__.__meta;
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$ICloneable$_clone$arity$1 = (function (this__6761__auto__){
var self__ = this;
var this__6761__auto____$1 = this;
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,self__.x_lim,self__.y_lim,self__.x_scale,self__.y_scale,self__.__meta,self__.__extmap,self__.__hash));
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$ICounted$_count$arity$1 = (function (this__6771__auto__){
var self__ = this;
var this__6771__auto____$1 = this;
return (6 + cljs.core.count(self__.__extmap));
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IHash$_hash$arity$1 = (function (this__6762__auto__){
var self__ = this;
var this__6762__auto____$1 = this;
var h__6588__auto__ = self__.__hash;
if(!((h__6588__auto__ == null))){
return h__6588__auto__;
} else {
var h__6588__auto____$1 = cljs.core.hash_imap(this__6762__auto____$1);
self__.__hash = h__6588__auto____$1;

return h__6588__auto____$1;
}
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IEquiv$_equiv$arity$2 = (function (this__6763__auto__,other__6764__auto__){
var self__ = this;
var this__6763__auto____$1 = this;
if(cljs.core.truth_((function (){var and__6141__auto__ = other__6764__auto__;
if(cljs.core.truth_(and__6141__auto__)){
var and__6141__auto____$1 = (this__6763__auto____$1.constructor === other__6764__auto__.constructor);
if(and__6141__auto____$1){
return cljs.core.equiv_map(this__6763__auto____$1,other__6764__auto__);
} else {
return and__6141__auto____$1;
}
} else {
return and__6141__auto__;
}
})())){
return true;
} else {
return false;
}
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IMap$_dissoc$arity$2 = (function (this__6776__auto__,k__6777__auto__){
var self__ = this;
var this__6776__auto____$1 = this;
if(cljs.core.contains_QMARK_(new cljs.core.PersistentHashSet(null, new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$x_DASH_scale,null,cljs.core.cst$kw$plot_DASH_size,null,cljs.core.cst$kw$y_DASH_lim,null,cljs.core.cst$kw$x_DASH_lim,null,cljs.core.cst$kw$ctx,null,cljs.core.cst$kw$y_DASH_scale,null], null), null),k__6777__auto__)){
return cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(cljs.core.with_meta(cljs.core.into.cljs$core$IFn$_invoke$arity$2(cljs.core.PersistentArrayMap.EMPTY,this__6776__auto____$1),self__.__meta),k__6777__auto__);
} else {
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,self__.x_lim,self__.y_lim,self__.x_scale,self__.y_scale,self__.__meta,cljs.core.not_empty(cljs.core.dissoc.cljs$core$IFn$_invoke$arity$2(self__.__extmap,k__6777__auto__)),null));
}
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IAssociative$_assoc$arity$3 = (function (this__6774__auto__,k__6775__auto__,G__59487){
var self__ = this;
var this__6774__auto____$1 = this;
var pred__59491 = cljs.core.keyword_identical_QMARK_;
var expr__59492 = k__6775__auto__;
if(cljs.core.truth_((pred__59491.cljs$core$IFn$_invoke$arity$2 ? pred__59491.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$ctx,expr__59492) : pred__59491.call(null,cljs.core.cst$kw$ctx,expr__59492)))){
return (new org.numenta.sanity.plots_canvas.XYPlot(G__59487,self__.plot_size,self__.x_lim,self__.y_lim,self__.x_scale,self__.y_scale,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__59491.cljs$core$IFn$_invoke$arity$2 ? pred__59491.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$plot_DASH_size,expr__59492) : pred__59491.call(null,cljs.core.cst$kw$plot_DASH_size,expr__59492)))){
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,G__59487,self__.x_lim,self__.y_lim,self__.x_scale,self__.y_scale,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__59491.cljs$core$IFn$_invoke$arity$2 ? pred__59491.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$x_DASH_lim,expr__59492) : pred__59491.call(null,cljs.core.cst$kw$x_DASH_lim,expr__59492)))){
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,G__59487,self__.y_lim,self__.x_scale,self__.y_scale,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__59491.cljs$core$IFn$_invoke$arity$2 ? pred__59491.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$y_DASH_lim,expr__59492) : pred__59491.call(null,cljs.core.cst$kw$y_DASH_lim,expr__59492)))){
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,self__.x_lim,G__59487,self__.x_scale,self__.y_scale,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__59491.cljs$core$IFn$_invoke$arity$2 ? pred__59491.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$x_DASH_scale,expr__59492) : pred__59491.call(null,cljs.core.cst$kw$x_DASH_scale,expr__59492)))){
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,self__.x_lim,self__.y_lim,G__59487,self__.y_scale,self__.__meta,self__.__extmap,null));
} else {
if(cljs.core.truth_((pred__59491.cljs$core$IFn$_invoke$arity$2 ? pred__59491.cljs$core$IFn$_invoke$arity$2(cljs.core.cst$kw$y_DASH_scale,expr__59492) : pred__59491.call(null,cljs.core.cst$kw$y_DASH_scale,expr__59492)))){
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,self__.x_lim,self__.y_lim,self__.x_scale,G__59487,self__.__meta,self__.__extmap,null));
} else {
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,self__.x_lim,self__.y_lim,self__.x_scale,self__.y_scale,self__.__meta,cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(self__.__extmap,k__6775__auto__,G__59487),null));
}
}
}
}
}
}
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$ISeqable$_seq$arity$1 = (function (this__6779__auto__){
var self__ = this;
var this__6779__auto____$1 = this;
return cljs.core.seq(cljs.core.concat.cljs$core$IFn$_invoke$arity$2(new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$ctx,self__.ctx],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$plot_DASH_size,self__.plot_size],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$x_DASH_lim,self__.x_lim],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$y_DASH_lim,self__.y_lim],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$x_DASH_scale,self__.x_scale],null)),(new cljs.core.PersistentVector(null,2,(5),cljs.core.PersistentVector.EMPTY_NODE,[cljs.core.cst$kw$y_DASH_scale,self__.y_scale],null))], null),self__.__extmap));
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$IWithMeta$_with_meta$arity$2 = (function (this__6766__auto__,G__59487){
var self__ = this;
var this__6766__auto____$1 = this;
return (new org.numenta.sanity.plots_canvas.XYPlot(self__.ctx,self__.plot_size,self__.x_lim,self__.y_lim,self__.x_scale,self__.y_scale,G__59487,self__.__extmap,self__.__hash));
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.cljs$core$ICollection$_conj$arity$2 = (function (this__6772__auto__,entry__6773__auto__){
var self__ = this;
var this__6772__auto____$1 = this;
if(cljs.core.vector_QMARK_(entry__6773__auto__)){
return cljs.core._assoc(this__6772__auto____$1,cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(0)),cljs.core._nth.cljs$core$IFn$_invoke$arity$2(entry__6773__auto__,(1)));
} else {
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(cljs.core._conj,this__6772__auto____$1,entry__6773__auto__);
}
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$ = true;

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$texts_BANG_$arity$5 = (function (_,x,y,txts,line_height){
var self__ = this;
var ___$1 = this;
return cljs.core.reduce.cljs$core$IFn$_invoke$arity$3(((function (___$1){
return (function (y_px,txt){
monet.canvas.text(self__.ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$text,txt,cljs.core.cst$kw$x,(self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x) : self__.x_scale.call(null,x)),cljs.core.cst$kw$y,y_px], null));

return (y_px + line_height);
});})(___$1))
,(self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y) : self__.y_scale.call(null,y)),txts);
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$frame_BANG_$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
var plot_rect = cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(self__.plot_size,cljs.core.cst$kw$x,(0),cljs.core.array_seq([cljs.core.cst$kw$y,(0)], 0));
var G__59494 = self__.ctx;
monet.canvas.stroke_style(G__59494,"black");

monet.canvas.stroke_rect(G__59494,plot_rect);

return G__59494;
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$bg_BANG_$arity$1 = (function (_){
var self__ = this;
var ___$1 = this;
var plot_rect = cljs.core.assoc.cljs$core$IFn$_invoke$arity$variadic(self__.plot_size,cljs.core.cst$kw$x,(0),cljs.core.array_seq([cljs.core.cst$kw$y,(0)], 0));
var G__59495 = self__.ctx;
monet.canvas.fill_style(G__59495,"white");

monet.canvas.fill_rect(G__59495,plot_rect);

return G__59495;
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$rect_BANG_$arity$5 = (function (_,x,y,w,h){
var self__ = this;
var ___$1 = this;
var xpx = (self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x) : self__.x_scale.call(null,x));
var ypx = (self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y) : self__.y_scale.call(null,y));
var G__59496 = self__.ctx;
monet.canvas.fill_rect(G__59496,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,xpx,cljs.core.cst$kw$y,ypx,cljs.core.cst$kw$w,((function (){var G__59497 = (x + w);
return (self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(G__59497) : self__.x_scale.call(null,G__59497));
})() - xpx),cljs.core.cst$kw$h,((function (){var G__59498 = (y + h);
return (self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(G__59498) : self__.y_scale.call(null,G__59498));
})() - ypx)], null));

return G__59496;
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$line_BANG_$arity$2 = (function (_,xys){
var self__ = this;
var ___$1 = this;
monet.canvas.begin_path(self__.ctx);

var seq__59499_59520 = cljs.core.seq(org.numenta.sanity.plots_canvas.indexed(xys));
var chunk__59500_59521 = null;
var count__59501_59522 = (0);
var i__59502_59523 = (0);
while(true){
if((i__59502_59523 < count__59501_59522)){
var vec__59503_59524 = chunk__59500_59521.cljs$core$IIndexed$_nth$arity$2(null,i__59502_59523);
var i_59525 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59503_59524,(0),null);
var vec__59504_59526 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59503_59524,(1),null);
var x_59527 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59504_59526,(0),null);
var y_59528 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59504_59526,(1),null);
var f_59529 = (((i_59525 === (0)))?monet.canvas.move_to:monet.canvas.line_to);
var G__59505_59530 = self__.ctx;
var G__59506_59531 = (self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x_59527) : self__.x_scale.call(null,x_59527));
var G__59507_59532 = (self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y_59528) : self__.y_scale.call(null,y_59528));
(f_59529.cljs$core$IFn$_invoke$arity$3 ? f_59529.cljs$core$IFn$_invoke$arity$3(G__59505_59530,G__59506_59531,G__59507_59532) : f_59529.call(null,G__59505_59530,G__59506_59531,G__59507_59532));

var G__59533 = seq__59499_59520;
var G__59534 = chunk__59500_59521;
var G__59535 = count__59501_59522;
var G__59536 = (i__59502_59523 + (1));
seq__59499_59520 = G__59533;
chunk__59500_59521 = G__59534;
count__59501_59522 = G__59535;
i__59502_59523 = G__59536;
continue;
} else {
var temp__4657__auto___59537 = cljs.core.seq(seq__59499_59520);
if(temp__4657__auto___59537){
var seq__59499_59538__$1 = temp__4657__auto___59537;
if(cljs.core.chunked_seq_QMARK_(seq__59499_59538__$1)){
var c__6956__auto___59539 = cljs.core.chunk_first(seq__59499_59538__$1);
var G__59540 = cljs.core.chunk_rest(seq__59499_59538__$1);
var G__59541 = c__6956__auto___59539;
var G__59542 = cljs.core.count(c__6956__auto___59539);
var G__59543 = (0);
seq__59499_59520 = G__59540;
chunk__59500_59521 = G__59541;
count__59501_59522 = G__59542;
i__59502_59523 = G__59543;
continue;
} else {
var vec__59508_59544 = cljs.core.first(seq__59499_59538__$1);
var i_59545 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59508_59544,(0),null);
var vec__59509_59546 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59508_59544,(1),null);
var x_59547 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59509_59546,(0),null);
var y_59548 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59509_59546,(1),null);
var f_59549 = (((i_59545 === (0)))?monet.canvas.move_to:monet.canvas.line_to);
var G__59510_59550 = self__.ctx;
var G__59511_59551 = (self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x_59547) : self__.x_scale.call(null,x_59547));
var G__59512_59552 = (self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y_59548) : self__.y_scale.call(null,y_59548));
(f_59549.cljs$core$IFn$_invoke$arity$3 ? f_59549.cljs$core$IFn$_invoke$arity$3(G__59510_59550,G__59511_59551,G__59512_59552) : f_59549.call(null,G__59510_59550,G__59511_59551,G__59512_59552));

var G__59553 = cljs.core.next(seq__59499_59538__$1);
var G__59554 = null;
var G__59555 = (0);
var G__59556 = (0);
seq__59499_59520 = G__59553;
chunk__59500_59521 = G__59554;
count__59501_59522 = G__59555;
i__59502_59523 = G__59556;
continue;
}
} else {
}
}
break;
}

return monet.canvas.stroke(self__.ctx);
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$point_BANG_$arity$4 = (function (_,x,y,radius_px){
var self__ = this;
var ___$1 = this;
var G__59513 = self__.ctx;
monet.canvas.circle(G__59513,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$x,(self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x) : self__.x_scale.call(null,x)),cljs.core.cst$kw$y,(self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y) : self__.y_scale.call(null,y)),cljs.core.cst$kw$r,radius_px], null));

monet.canvas.fill(G__59513);

monet.canvas.stroke(G__59513);

return G__59513;
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$grid_BANG_$arity$2 = (function (_,p__59514){
var self__ = this;
var map__59515 = p__59514;
var map__59515__$1 = ((((!((map__59515 == null)))?((((map__59515.cljs$lang$protocol_mask$partition0$ & (64))) || (map__59515.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__59515):map__59515);
var grid_every = cljs.core.get.cljs$core$IFn$_invoke$arity$3(map__59515__$1,cljs.core.cst$kw$grid_DASH_every,(1));
var ___$1 = this;
monet.canvas.save(self__.ctx);

var vec__59517_59557 = self__.x_lim;
var x_lo_59558 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59517_59557,(0),null);
var x_hi_59559 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59517_59557,(1),null);
var vec__59518_59560 = self__.y_lim;
var y_lo_59561 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59518_59560,(0),null);
var y_hi_59562 = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__59518_59560,(1),null);
org.numenta.sanity.plots_canvas.draw_grid(self__.ctx,new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(self__.plot_size)], null),new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(0),cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(self__.plot_size)], null),cljs.core.map.cljs$core$IFn$_invoke$arity$2(self__.x_scale,cljs.core.range.cljs$core$IFn$_invoke$arity$3(cljs.core.long$(x_lo_59558),(cljs.core.long$(x_hi_59559) + (1)),grid_every)),cljs.core.map.cljs$core$IFn$_invoke$arity$2(self__.y_scale,cljs.core.range.cljs$core$IFn$_invoke$arity$3(cljs.core.long$(y_lo_59561),(cljs.core.long$(y_hi_59562) + (1)),grid_every)));

return monet.canvas.restore(self__.ctx);
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$__GT_px$arity$3 = (function (_,x,y){
var self__ = this;
var ___$1 = this;
return new cljs.core.PersistentVector(null, 2, 5, cljs.core.PersistentVector.EMPTY_NODE, [(self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x) : self__.x_scale.call(null,x)),(self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y) : self__.y_scale.call(null,y))], null);
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$text_BANG_$arity$4 = (function (_,x,y,txt){
var self__ = this;
var ___$1 = this;
return monet.canvas.text(self__.ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$text,txt,cljs.core.cst$kw$x,(self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x) : self__.x_scale.call(null,x)),cljs.core.cst$kw$y,(self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y) : self__.y_scale.call(null,y))], null));
});

org.numenta.sanity.plots_canvas.XYPlot.prototype.org$numenta$sanity$plots_canvas$PPlot$text_rotated_BANG_$arity$4 = (function (_,x,y,txt){
var self__ = this;
var ___$1 = this;
return org.numenta.sanity.plots_canvas.text_rotated(self__.ctx,new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$text,txt,cljs.core.cst$kw$x,(self__.x_scale.cljs$core$IFn$_invoke$arity$1 ? self__.x_scale.cljs$core$IFn$_invoke$arity$1(x) : self__.x_scale.call(null,x)),cljs.core.cst$kw$y,(self__.y_scale.cljs$core$IFn$_invoke$arity$1 ? self__.y_scale.cljs$core$IFn$_invoke$arity$1(y) : self__.y_scale.call(null,y))], null));
});

org.numenta.sanity.plots_canvas.XYPlot.getBasis = (function (){
return new cljs.core.PersistentVector(null, 6, 5, cljs.core.PersistentVector.EMPTY_NODE, [cljs.core.cst$sym$ctx,cljs.core.cst$sym$plot_DASH_size,cljs.core.cst$sym$x_DASH_lim,cljs.core.cst$sym$y_DASH_lim,cljs.core.cst$sym$x_DASH_scale,cljs.core.cst$sym$y_DASH_scale], null);
});

org.numenta.sanity.plots_canvas.XYPlot.cljs$lang$type = true;

org.numenta.sanity.plots_canvas.XYPlot.cljs$lang$ctorPrSeq = (function (this__6801__auto__){
return cljs.core._conj(cljs.core.List.EMPTY,"org.numenta.sanity.plots-canvas/XYPlot");
});

org.numenta.sanity.plots_canvas.XYPlot.cljs$lang$ctorPrWriter = (function (this__6801__auto__,writer__6802__auto__){
return cljs.core._write(writer__6802__auto__,"org.numenta.sanity.plots-canvas/XYPlot");
});

org.numenta.sanity.plots_canvas.__GT_XYPlot = (function org$numenta$sanity$plots_canvas$__GT_XYPlot(ctx,plot_size,x_lim,y_lim,x_scale,y_scale){
return (new org.numenta.sanity.plots_canvas.XYPlot(ctx,plot_size,x_lim,y_lim,x_scale,y_scale,null,null,null));
});

org.numenta.sanity.plots_canvas.map__GT_XYPlot = (function org$numenta$sanity$plots_canvas$map__GT_XYPlot(G__59489){
return (new org.numenta.sanity.plots_canvas.XYPlot(cljs.core.cst$kw$ctx.cljs$core$IFn$_invoke$arity$1(G__59489),cljs.core.cst$kw$plot_DASH_size.cljs$core$IFn$_invoke$arity$1(G__59489),cljs.core.cst$kw$x_DASH_lim.cljs$core$IFn$_invoke$arity$1(G__59489),cljs.core.cst$kw$y_DASH_lim.cljs$core$IFn$_invoke$arity$1(G__59489),cljs.core.cst$kw$x_DASH_scale.cljs$core$IFn$_invoke$arity$1(G__59489),cljs.core.cst$kw$y_DASH_scale.cljs$core$IFn$_invoke$arity$1(G__59489),null,cljs.core.dissoc.cljs$core$IFn$_invoke$arity$variadic(G__59489,cljs.core.cst$kw$ctx,cljs.core.array_seq([cljs.core.cst$kw$plot_DASH_size,cljs.core.cst$kw$x_DASH_lim,cljs.core.cst$kw$y_DASH_lim,cljs.core.cst$kw$x_DASH_scale,cljs.core.cst$kw$y_DASH_scale], 0)),null));
});

/**
 * Assumes ctx is already translated.
 */
org.numenta.sanity.plots_canvas.xy_plot = (function org$numenta$sanity$plots_canvas$xy_plot(ctx,p__59563,x_lim,y_lim){
var map__59566 = p__59563;
var map__59566__$1 = ((((!((map__59566 == null)))?((((map__59566.cljs$lang$protocol_mask$partition0$ & (64))) || (map__59566.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__59566):map__59566);
var plot_size = map__59566__$1;
var w = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__59566__$1,cljs.core.cst$kw$w);
var h = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__59566__$1,cljs.core.cst$kw$h);
var x_scale = org.numenta.sanity.plots_canvas.scale_fn(x_lim,cljs.core.cst$kw$w.cljs$core$IFn$_invoke$arity$1(plot_size));
var y_scale = org.numenta.sanity.plots_canvas.scale_fn(y_lim,cljs.core.cst$kw$h.cljs$core$IFn$_invoke$arity$1(plot_size));
return org.numenta.sanity.plots_canvas.map__GT_XYPlot(new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$ctx,ctx,cljs.core.cst$kw$plot_DASH_size,plot_size,cljs.core.cst$kw$x_DASH_lim,x_lim,cljs.core.cst$kw$y_DASH_lim,y_lim,cljs.core.cst$kw$x_DASH_scale,x_scale,cljs.core.cst$kw$y_DASH_scale,y_scale], null));
});
