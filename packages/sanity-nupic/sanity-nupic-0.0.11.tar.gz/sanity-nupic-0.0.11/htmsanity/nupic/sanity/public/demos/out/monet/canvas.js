// Compiled by ClojureScript 1.7.228 {:static-fns true, :optimize-constants true}
goog.provide('monet.canvas');
goog.require('cljs.core');
goog.require('monet.core');
monet.canvas.get_context = (function monet$canvas$get_context(canvas,type){
return canvas.getContext(cljs.core.name(type));
});
/**
 * Starts a new path by resetting the list of sub-paths.
 * Call this method when you want to create a new path.
 */
monet.canvas.begin_path = (function monet$canvas$begin_path(ctx){
ctx.beginPath();

return ctx;
});
/**
 * Tries to draw a straight line from the current point to the start.
 * If the shape has already been closed or has only one point, this
 * function does nothing.
 */
monet.canvas.close_path = (function monet$canvas$close_path(ctx){
ctx.closePath();

return ctx;
});
/**
 * Saves the current drawing style state using a stack so you can revert
 * any change you make to it using restore.
 */
monet.canvas.save = (function monet$canvas$save(ctx){
ctx.save();

return ctx;
});
/**
 * Restores the drawing style state to the last element on the 'state stack'
 * saved by save.
 */
monet.canvas.restore = (function monet$canvas$restore(ctx){
ctx.restore();

return ctx;
});
/**
 * Rotate the context 
 */
monet.canvas.rotate = (function monet$canvas$rotate(ctx,angle){
ctx.rotate(angle);

return ctx;
});
/**
 * Scales the context by a floating-point factor in each direction
 */
monet.canvas.scale = (function monet$canvas$scale(ctx,x,y){
ctx.scale(x,y);

return ctx;
});
/**
 * Moves the origin point of the context to (x, y).
 */
monet.canvas.translate = (function monet$canvas$translate(ctx,x,y){
ctx.translate(x,y);

return ctx;
});
/**
 * Multiplies a custom transformation matrix to the existing
 * HTML5 canvas transformation according to the follow convention:
 * 
 * [ x']   [ m11 m21 dx ] [ x ]
 * [ y'] = [ m12 m22 dy ] [ y ]
 * [ 1 ]   [ 0   0   1  ] [ 1 ]
 */
monet.canvas.transform = (function monet$canvas$transform(var_args){
var args46905 = [];
var len__7211__auto___46911 = arguments.length;
var i__7212__auto___46912 = (0);
while(true){
if((i__7212__auto___46912 < len__7211__auto___46911)){
args46905.push((arguments[i__7212__auto___46912]));

var G__46913 = (i__7212__auto___46912 + (1));
i__7212__auto___46912 = G__46913;
continue;
} else {
}
break;
}

var G__46907 = args46905.length;
switch (G__46907) {
case 7:
return monet.canvas.transform.cljs$core$IFn$_invoke$arity$7((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]),(arguments[(4)]),(arguments[(5)]),(arguments[(6)]));

break;
case 2:
return monet.canvas.transform.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args46905.length)].join('')));

}
});

monet.canvas.transform.cljs$core$IFn$_invoke$arity$7 = (function (ctx,m11,m12,m21,m22,dx,dy){
ctx.transform(m11,m12,m21,m22,dx,dy);

return ctx;
});

monet.canvas.transform.cljs$core$IFn$_invoke$arity$2 = (function (ctx,p__46908){
var map__46909 = p__46908;
var map__46909__$1 = ((((!((map__46909 == null)))?((((map__46909.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46909.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46909):map__46909);
var m11 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46909__$1,cljs.core.cst$kw$m11);
var m12 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46909__$1,cljs.core.cst$kw$m12);
var m21 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46909__$1,cljs.core.cst$kw$m21);
var m22 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46909__$1,cljs.core.cst$kw$m22);
var dx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46909__$1,cljs.core.cst$kw$dx);
var dy = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46909__$1,cljs.core.cst$kw$dy);
ctx.transform(m11,m12,m21,m22,dx,dy);

return ctx;
});

monet.canvas.transform.cljs$lang$maxFixedArity = 7;
/**
 * Fills the subpaths with the current fill style.
 */
monet.canvas.fill = (function monet$canvas$fill(ctx){
ctx.fill();

return ctx;
});
/**
 * Strokes the subpaths with the current stroke style.
 */
monet.canvas.stroke = (function monet$canvas$stroke(ctx){
ctx.stroke();

return ctx;
});
/**
 * Further constrains the clipping region to the current path.
 */
monet.canvas.clip = (function monet$canvas$clip(ctx){
ctx.clip();

return ctx;
});
/**
 * Sets all pixels in the rectangle defined by starting point (x, y)
 * and size (w, h) to transparent black.
 */
monet.canvas.clear_rect = (function monet$canvas$clear_rect(ctx,p__46915){
var map__46918 = p__46915;
var map__46918__$1 = ((((!((map__46918 == null)))?((((map__46918.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46918.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46918):map__46918);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46918__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46918__$1,cljs.core.cst$kw$y);
var w = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46918__$1,cljs.core.cst$kw$w);
var h = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46918__$1,cljs.core.cst$kw$h);
ctx.clearRect(x,y,w,h);

return ctx;
});
/**
 * Paints a rectangle which has a starting point at (x, y) and has a
 * w width and an h height onto the canvas, using the current stroke
 * style.
 */
monet.canvas.stroke_rect = (function monet$canvas$stroke_rect(ctx,p__46920){
var map__46923 = p__46920;
var map__46923__$1 = ((((!((map__46923 == null)))?((((map__46923.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46923.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46923):map__46923);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46923__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46923__$1,cljs.core.cst$kw$y);
var w = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46923__$1,cljs.core.cst$kw$w);
var h = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46923__$1,cljs.core.cst$kw$h);
ctx.strokeRect(x,y,w,h);

return ctx;
});
/**
 * Draws a filled rectangle at (x, y) position whose size is determined
 * by width w and height h.
 */
monet.canvas.fill_rect = (function monet$canvas$fill_rect(ctx,p__46925){
var map__46928 = p__46925;
var map__46928__$1 = ((((!((map__46928 == null)))?((((map__46928.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46928.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46928):map__46928);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46928__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46928__$1,cljs.core.cst$kw$y);
var w = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46928__$1,cljs.core.cst$kw$w);
var h = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46928__$1,cljs.core.cst$kw$h);
ctx.fillRect(x,y,w,h);

return ctx;
});
/**
 * Draws an arc at position (x, y) with radius r, beginning at start-angle,
 * finishing at end-angle, in the direction specified.
 */
monet.canvas.arc = (function monet$canvas$arc(ctx,p__46930){
var map__46933 = p__46930;
var map__46933__$1 = ((((!((map__46933 == null)))?((((map__46933.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46933.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46933):map__46933);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46933__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46933__$1,cljs.core.cst$kw$y);
var r = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46933__$1,cljs.core.cst$kw$r);
var start_angle = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46933__$1,cljs.core.cst$kw$start_DASH_angle);
var end_angle = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46933__$1,cljs.core.cst$kw$end_DASH_angle);
var counter_clockwise_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46933__$1,cljs.core.cst$kw$counter_DASH_clockwise_QMARK_);
ctx.arc(x,y,r,start_angle,end_angle,counter_clockwise_QMARK_);

return ctx;
});
monet.canvas.two_pi = ((2) * Math.PI);
/**
 * Draws an ellipse at position (x, y) with radius (rw, rh)
 */
monet.canvas.ellipse = (function monet$canvas$ellipse(ctx,p__46935){
var map__46938 = p__46935;
var map__46938__$1 = ((((!((map__46938 == null)))?((((map__46938.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46938.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46938):map__46938);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46938__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46938__$1,cljs.core.cst$kw$y);
var rw = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46938__$1,cljs.core.cst$kw$rw);
var rh = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46938__$1,cljs.core.cst$kw$rh);
return monet.canvas.restore(monet.canvas.close_path(monet.canvas.arc(monet.canvas.begin_path(monet.canvas.scale(monet.canvas.save(ctx),(1),(rh / rw))),new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$x,x,cljs.core.cst$kw$y,y,cljs.core.cst$kw$r,rw,cljs.core.cst$kw$start_DASH_angle,(0),cljs.core.cst$kw$end_DASH_angle,monet.canvas.two_pi,cljs.core.cst$kw$counter_DASH_clockwise_QMARK_,false], null))));
});
/**
 * Draws a circle at position (x, y) with radius r
 */
monet.canvas.circle = (function monet$canvas$circle(ctx,p__46940){
var map__46943 = p__46940;
var map__46943__$1 = ((((!((map__46943 == null)))?((((map__46943.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46943.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46943):map__46943);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46943__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46943__$1,cljs.core.cst$kw$y);
var r = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46943__$1,cljs.core.cst$kw$r);
return monet.canvas.close_path(monet.canvas.arc(monet.canvas.begin_path(ctx),new cljs.core.PersistentArrayMap(null, 6, [cljs.core.cst$kw$x,x,cljs.core.cst$kw$y,y,cljs.core.cst$kw$r,r,cljs.core.cst$kw$start_DASH_angle,(0),cljs.core.cst$kw$end_DASH_angle,monet.canvas.two_pi,cljs.core.cst$kw$counter_DASH_clockwise_QMARK_,true], null)));
});
/**
 * Paints the given text at a starting point at (x, y), using the
 * current stroke style.
 */
monet.canvas.text = (function monet$canvas$text(ctx,p__46945){
var map__46948 = p__46945;
var map__46948__$1 = ((((!((map__46948 == null)))?((((map__46948.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46948.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46948):map__46948);
var text__$1 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46948__$1,cljs.core.cst$kw$text);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46948__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46948__$1,cljs.core.cst$kw$y);
ctx.fillText(text__$1,x,y);

return ctx;
});
/**
 * Sets the font. Default value 10px sans-serif.
 */
monet.canvas.font_style = (function monet$canvas$font_style(ctx,font){
ctx.font = font;

return ctx;
});
/**
 * Color or style to use inside shapes. Default #000 (black).
 */
monet.canvas.fill_style = (function monet$canvas$fill_style(ctx,color){
ctx.fillStyle = cljs.core.name(color);

return ctx;
});
/**
 * Color or style to use for the lines around shapes. Default #000 (black).
 */
monet.canvas.stroke_style = (function monet$canvas$stroke_style(ctx,color){
ctx.strokeStyle = cljs.core.name(color);

return ctx;
});
/**
 * Sets the line width. Default 1.0
 */
monet.canvas.stroke_width = (function monet$canvas$stroke_width(ctx,w){
ctx.lineWidth = w;

return ctx;
});
/**
 * Sets the line cap. Possible values (as string or keyword):
 * butt (default), round, square
 */
monet.canvas.stroke_cap = (function monet$canvas$stroke_cap(ctx,cap){
ctx.lineCap = cljs.core.name(cap);

return ctx;
});
/**
 * Can be set, to change the line join style. Possible values (as string
 * or keyword): bevel, round, and miter. Other values are ignored.
 */
monet.canvas.stroke_join = (function monet$canvas$stroke_join(ctx,join){
ctx.lineJoin = cljs.core.name(join);

return ctx;
});
/**
 * Moves the starting point of a new subpath to the (x, y) coordinates.
 */
monet.canvas.move_to = (function monet$canvas$move_to(ctx,x,y){
ctx.moveTo(x,y);

return ctx;
});
/**
 * Connects the last point in the subpath to the x, y coordinates with a
 * straight line.
 */
monet.canvas.line_to = (function monet$canvas$line_to(ctx,x,y){
ctx.lineTo(x,y);

return ctx;
});
/**
 * Global Alpha value that is applied to shapes and images before they are
 * composited onto the canvas. Default 1.0 (opaque).
 */
monet.canvas.alpha = (function monet$canvas$alpha(ctx,a){
ctx.globalAlpha = a;

return ctx;
});
/**
 * With Global Alpha applied this sets how shapes and images are drawn
 * onto the existing bitmap. Possible values (as string or keyword):
 * source-atop, source-in, source-out, source-over (default),
 * destination-atop, destination-in, destination-out, destination-over,
 * lighter, darker, copy, xor
 */
monet.canvas.composition_operation = (function monet$canvas$composition_operation(ctx,operation){
ctx.globalCompositionOperation = cljs.core.name(operation);

return ctx;
});
/**
 * Sets the text alignment attribute. Possible values (specified
 * as a string or keyword): start (default), end, left, right or
 * center.
 */
monet.canvas.text_align = (function monet$canvas$text_align(ctx,alignment){
ctx.textAlign = cljs.core.name(alignment);

return ctx;
});
/**
 * Sets the text baseline attribute. Possible values (specified
 * as a string or keyword): top, hanging, middle, alphabetic (default),
 * ideographic, bottom
 */
monet.canvas.text_baseline = (function monet$canvas$text_baseline(ctx,alignment){
ctx.textBaseline = cljs.core.name(alignment);

return ctx;
});
/**
 * Gets the pixel value as a hash map of RGBA values
 */
monet.canvas.get_pixel = (function monet$canvas$get_pixel(ctx,x,y){
var imgd = ctx.getImageData(x,y,(1),(1)).data;
return new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$red,(imgd[(0)]),cljs.core.cst$kw$green,(imgd[(1)]),cljs.core.cst$kw$blue,(imgd[(2)]),cljs.core.cst$kw$alpha,(imgd[(3)])], null);
});
/**
 * Draws the image onto the canvas at the given position.
 * If a map of params is given, the number of entries is used to
 * determine the underlying call to make.
 */
monet.canvas.draw_image = (function monet$canvas$draw_image(var_args){
var args46950 = [];
var len__7211__auto___46959 = arguments.length;
var i__7212__auto___46960 = (0);
while(true){
if((i__7212__auto___46960 < len__7211__auto___46959)){
args46950.push((arguments[i__7212__auto___46960]));

var G__46961 = (i__7212__auto___46960 + (1));
i__7212__auto___46960 = G__46961;
continue;
} else {
}
break;
}

var G__46952 = args46950.length;
switch (G__46952) {
case 4:
return monet.canvas.draw_image.cljs$core$IFn$_invoke$arity$4((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]));

break;
case 3:
return monet.canvas.draw_image.cljs$core$IFn$_invoke$arity$3((arguments[(0)]),(arguments[(1)]),(arguments[(2)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args46950.length)].join('')));

}
});

monet.canvas.draw_image.cljs$core$IFn$_invoke$arity$4 = (function (ctx,img,x,y){
ctx.drawImage(img,x,y);

return ctx;
});

monet.canvas.draw_image.cljs$core$IFn$_invoke$arity$3 = (function (ctx,img,p__46953){
var map__46954 = p__46953;
var map__46954__$1 = ((((!((map__46954 == null)))?((((map__46954.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46954.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46954):map__46954);
var params = map__46954__$1;
var sh = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$sh);
var sw = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$sw);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$y);
var dh = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$dh);
var dx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$dx);
var w = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$w);
var sy = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$sy);
var dy = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$dy);
var h = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$h);
var dw = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$dw);
var sx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46954__$1,cljs.core.cst$kw$sx);
var pred__46956_46963 = cljs.core._EQ_;
var expr__46957_46964 = cljs.core.count(params);
if(cljs.core.truth_((pred__46956_46963.cljs$core$IFn$_invoke$arity$2 ? pred__46956_46963.cljs$core$IFn$_invoke$arity$2((2),expr__46957_46964) : pred__46956_46963.call(null,(2),expr__46957_46964)))){
ctx.drawImage(img,x,y);
} else {
if(cljs.core.truth_((pred__46956_46963.cljs$core$IFn$_invoke$arity$2 ? pred__46956_46963.cljs$core$IFn$_invoke$arity$2((4),expr__46957_46964) : pred__46956_46963.call(null,(4),expr__46957_46964)))){
ctx.drawImage(img,x,y,w,h);
} else {
if(cljs.core.truth_((pred__46956_46963.cljs$core$IFn$_invoke$arity$2 ? pred__46956_46963.cljs$core$IFn$_invoke$arity$2((8),expr__46957_46964) : pred__46956_46963.call(null,(8),expr__46957_46964)))){
ctx.drawImage(img,sx,sy,sw,sh,dx,dy,dw,dh);
} else {
throw (new Error([cljs.core.str("No matching clause: "),cljs.core.str(expr__46957_46964)].join('')));
}
}
}

return ctx;
});

monet.canvas.draw_image.cljs$lang$maxFixedArity = 4;
monet.canvas.quadratic_curve_to = (function monet$canvas$quadratic_curve_to(var_args){
var args46965 = [];
var len__7211__auto___46971 = arguments.length;
var i__7212__auto___46972 = (0);
while(true){
if((i__7212__auto___46972 < len__7211__auto___46971)){
args46965.push((arguments[i__7212__auto___46972]));

var G__46973 = (i__7212__auto___46972 + (1));
i__7212__auto___46972 = G__46973;
continue;
} else {
}
break;
}

var G__46967 = args46965.length;
switch (G__46967) {
case 5:
return monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$5((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]),(arguments[(4)]));

break;
case 2:
return monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args46965.length)].join('')));

}
});

monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$5 = (function (ctx,cpx,cpy,x,y){
ctx.quadraticCurveTo(cpx,cpy,x,y);

return ctx;
});

monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$2 = (function (ctx,p__46968){
var map__46969 = p__46968;
var map__46969__$1 = ((((!((map__46969 == null)))?((((map__46969.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46969.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46969):map__46969);
var cpx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46969__$1,cljs.core.cst$kw$cpx);
var cpy = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46969__$1,cljs.core.cst$kw$cpy);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46969__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46969__$1,cljs.core.cst$kw$y);
ctx.quadraticCurveTo(cpx,cpy,x,y);

return ctx;
});

monet.canvas.quadratic_curve_to.cljs$lang$maxFixedArity = 5;
monet.canvas.bezier_curve_to = (function monet$canvas$bezier_curve_to(var_args){
var args46975 = [];
var len__7211__auto___46981 = arguments.length;
var i__7212__auto___46982 = (0);
while(true){
if((i__7212__auto___46982 < len__7211__auto___46981)){
args46975.push((arguments[i__7212__auto___46982]));

var G__46983 = (i__7212__auto___46982 + (1));
i__7212__auto___46982 = G__46983;
continue;
} else {
}
break;
}

var G__46977 = args46975.length;
switch (G__46977) {
case 7:
return monet.canvas.bezier_curve_to.cljs$core$IFn$_invoke$arity$7((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),(arguments[(3)]),(arguments[(4)]),(arguments[(5)]),(arguments[(6)]));

break;
case 2:
return monet.canvas.bezier_curve_to.cljs$core$IFn$_invoke$arity$2((arguments[(0)]),(arguments[(1)]));

break;
default:
throw (new Error([cljs.core.str("Invalid arity: "),cljs.core.str(args46975.length)].join('')));

}
});

monet.canvas.bezier_curve_to.cljs$core$IFn$_invoke$arity$7 = (function (ctx,cp1x,cp1y,cp2x,cp2y,x,y){
ctx.bezierCurveTo(cp1x,cp1y,cp2x,cp2y,x,y);

return ctx;
});

monet.canvas.bezier_curve_to.cljs$core$IFn$_invoke$arity$2 = (function (ctx,p__46978){
var map__46979 = p__46978;
var map__46979__$1 = ((((!((map__46979 == null)))?((((map__46979.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46979.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46979):map__46979);
var cp1x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46979__$1,cljs.core.cst$kw$cp1x);
var cp1y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46979__$1,cljs.core.cst$kw$cp1y);
var cp2x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46979__$1,cljs.core.cst$kw$cp2x);
var cp2y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46979__$1,cljs.core.cst$kw$cp2y);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46979__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46979__$1,cljs.core.cst$kw$y);
ctx.bezierCurveTo(cp1x,cp1y,cp2x,cp2y,x,y);

return ctx;
});

monet.canvas.bezier_curve_to.cljs$lang$maxFixedArity = 7;
monet.canvas.rounded_rect = (function monet$canvas$rounded_rect(ctx,p__46985){
var map__46988 = p__46985;
var map__46988__$1 = ((((!((map__46988 == null)))?((((map__46988.cljs$lang$protocol_mask$partition0$ & (64))) || (map__46988.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__46988):map__46988);
var x = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46988__$1,cljs.core.cst$kw$x);
var y = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46988__$1,cljs.core.cst$kw$y);
var w = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46988__$1,cljs.core.cst$kw$w);
var h = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46988__$1,cljs.core.cst$kw$h);
var r = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__46988__$1,cljs.core.cst$kw$r);

monet.canvas.stroke(monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$5(monet.canvas.line_to(monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$5(monet.canvas.line_to(monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$5(monet.canvas.line_to(monet.canvas.quadratic_curve_to.cljs$core$IFn$_invoke$arity$5(monet.canvas.line_to(monet.canvas.move_to(monet.canvas.begin_path(ctx),x,(y + r)),x,((y + h) - r)),x,(y + h),(x + r),(y + h)),((x + w) - r),(y + h)),(x + w),(y + h),(x + w),((y + h) - r)),(x + w),(y + r)),(x + w),y,((x + w) - r),y),(x + r),y),x,y,x,(y + r)));

return ctx;
});
monet.canvas.add_entity = (function monet$canvas$add_entity(mc,k,ent){
return (cljs.core.cst$kw$entities.cljs$core$IFn$_invoke$arity$1(mc)[k] = ent);
});
monet.canvas.remove_entity = (function monet$canvas$remove_entity(mc,k){
return delete cljs.core.cst$kw$entities.cljs$core$IFn$_invoke$arity$1(mc)[k];
});
monet.canvas.get_entity = (function monet$canvas$get_entity(mc,k){
return cljs.core.cst$kw$value.cljs$core$IFn$_invoke$arity$1((cljs.core.cst$kw$entities.cljs$core$IFn$_invoke$arity$1(mc)[k]));
});
monet.canvas.update_entity = (function monet$canvas$update_entity(var_args){
var args__7218__auto__ = [];
var len__7211__auto___46994 = arguments.length;
var i__7212__auto___46995 = (0);
while(true){
if((i__7212__auto___46995 < len__7211__auto___46994)){
args__7218__auto__.push((arguments[i__7212__auto___46995]));

var G__46996 = (i__7212__auto___46995 + (1));
i__7212__auto___46995 = G__46996;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((3) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((3)),(0))):null);
return monet.canvas.update_entity.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),(arguments[(1)]),(arguments[(2)]),argseq__7219__auto__);
});

monet.canvas.update_entity.cljs$core$IFn$_invoke$arity$variadic = (function (mc,k,func,extra){
var cur = (cljs.core.cst$kw$entities.cljs$core$IFn$_invoke$arity$1(mc)[k]);
var res = cljs.core.apply.cljs$core$IFn$_invoke$arity$3(func,cur,extra);
return (cljs.core.cst$kw$entities.cljs$core$IFn$_invoke$arity$1(mc)[k] = res);
});

monet.canvas.update_entity.cljs$lang$maxFixedArity = (3);

monet.canvas.update_entity.cljs$lang$applyTo = (function (seq46990){
var G__46991 = cljs.core.first(seq46990);
var seq46990__$1 = cljs.core.next(seq46990);
var G__46992 = cljs.core.first(seq46990__$1);
var seq46990__$2 = cljs.core.next(seq46990__$1);
var G__46993 = cljs.core.first(seq46990__$2);
var seq46990__$3 = cljs.core.next(seq46990__$2);
return monet.canvas.update_entity.cljs$core$IFn$_invoke$arity$variadic(G__46991,G__46992,G__46993,seq46990__$3);
});
monet.canvas.clear_BANG_ = (function monet$canvas$clear_BANG_(mc){
var ks = cljs.core.js_keys(cljs.core.cst$kw$entities.cljs$core$IFn$_invoke$arity$1(mc));
var seq__47001 = cljs.core.seq(ks);
var chunk__47002 = null;
var count__47003 = (0);
var i__47004 = (0);
while(true){
if((i__47004 < count__47003)){
var k = chunk__47002.cljs$core$IIndexed$_nth$arity$2(null,i__47004);
monet.canvas.remove_entity(mc,k);

var G__47005 = seq__47001;
var G__47006 = chunk__47002;
var G__47007 = count__47003;
var G__47008 = (i__47004 + (1));
seq__47001 = G__47005;
chunk__47002 = G__47006;
count__47003 = G__47007;
i__47004 = G__47008;
continue;
} else {
var temp__4657__auto__ = cljs.core.seq(seq__47001);
if(temp__4657__auto__){
var seq__47001__$1 = temp__4657__auto__;
if(cljs.core.chunked_seq_QMARK_(seq__47001__$1)){
var c__6956__auto__ = cljs.core.chunk_first(seq__47001__$1);
var G__47009 = cljs.core.chunk_rest(seq__47001__$1);
var G__47010 = c__6956__auto__;
var G__47011 = cljs.core.count(c__6956__auto__);
var G__47012 = (0);
seq__47001 = G__47009;
chunk__47002 = G__47010;
count__47003 = G__47011;
i__47004 = G__47012;
continue;
} else {
var k = cljs.core.first(seq__47001__$1);
monet.canvas.remove_entity(mc,k);

var G__47013 = cljs.core.next(seq__47001__$1);
var G__47014 = null;
var G__47015 = (0);
var G__47016 = (0);
seq__47001 = G__47013;
chunk__47002 = G__47014;
count__47003 = G__47015;
i__47004 = G__47016;
continue;
}
} else {
return null;
}
}
break;
}
});
monet.canvas.entity = (function monet$canvas$entity(v,update,draw){
return new cljs.core.PersistentArrayMap(null, 3, [cljs.core.cst$kw$value,v,cljs.core.cst$kw$draw,draw,cljs.core.cst$kw$update,update], null);
});
monet.canvas.attr = (function monet$canvas$attr(e,a){
return e.getAttribute(a);
});
monet.canvas.draw_loop = (function monet$canvas$draw_loop(p__47017){
var map__47028 = p__47017;
var map__47028__$1 = ((((!((map__47028 == null)))?((((map__47028.cljs$lang$protocol_mask$partition0$ & (64))) || (map__47028.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__47028):map__47028);
var mc = map__47028__$1;
var canvas = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47028__$1,cljs.core.cst$kw$canvas);
var updating_QMARK_ = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47028__$1,cljs.core.cst$kw$updating_QMARK_);
var ctx = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47028__$1,cljs.core.cst$kw$ctx);
var active = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47028__$1,cljs.core.cst$kw$active);
var entities = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47028__$1,cljs.core.cst$kw$entities);
monet.canvas.clear_rect(ctx,new cljs.core.PersistentArrayMap(null, 4, [cljs.core.cst$kw$x,(0),cljs.core.cst$kw$y,(0),cljs.core.cst$kw$w,monet.canvas.attr(canvas,"width"),cljs.core.cst$kw$h,monet.canvas.attr(canvas,"height")], null));

if(cljs.core.truth_((cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(active) : cljs.core.deref.call(null,active)))){
var ks_47038 = cljs.core.js_keys(entities);
var cnt_47039 = ks_47038.length;
var i_47040 = (0);
while(true){
if((i_47040 < cnt_47039)){
var k_47041 = (ks_47038[i_47040]);
var map__47030_47042 = (entities[k_47041]);
var map__47030_47043__$1 = ((((!((map__47030_47042 == null)))?((((map__47030_47042.cljs$lang$protocol_mask$partition0$ & (64))) || (map__47030_47042.cljs$core$ISeq$))?true:false):false))?cljs.core.apply.cljs$core$IFn$_invoke$arity$2(cljs.core.hash_map,map__47030_47042):map__47030_47042);
var ent_47044 = map__47030_47043__$1;
var draw_47045 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47030_47043__$1,cljs.core.cst$kw$draw);
var update_47046 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47030_47043__$1,cljs.core.cst$kw$update);
var value_47047 = cljs.core.get.cljs$core$IFn$_invoke$arity$2(map__47030_47043__$1,cljs.core.cst$kw$value);
if(cljs.core.truth_((function (){var and__6141__auto__ = update_47046;
if(cljs.core.truth_(and__6141__auto__)){
return (cljs.core.deref.cljs$core$IFn$_invoke$arity$1 ? cljs.core.deref.cljs$core$IFn$_invoke$arity$1(updating_QMARK_) : cljs.core.deref.call(null,updating_QMARK_));
} else {
return and__6141__auto__;
}
})())){
var updated_47048 = (function (){var or__6153__auto__ = (function (){try{return (update_47046.cljs$core$IFn$_invoke$arity$1 ? update_47046.cljs$core$IFn$_invoke$arity$1(value_47047) : update_47046.call(null,value_47047));
}catch (e47033){if((e47033 instanceof Error)){
var e = e47033;
console.log(e);

return value_47047;
} else {
throw e47033;

}
}})();
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return value_47047;
}
})();
if(cljs.core.truth_((entities[k_47041]))){
(entities[k_47041] = cljs.core.assoc.cljs$core$IFn$_invoke$arity$3(ent_47044,cljs.core.cst$kw$value,updated_47048));
} else {
}
} else {
}

if(cljs.core.truth_(draw_47045)){
try{var G__47035_47049 = ctx;
var G__47036_47050 = cljs.core.cst$kw$value.cljs$core$IFn$_invoke$arity$1((entities[k_47041]));
(draw_47045.cljs$core$IFn$_invoke$arity$2 ? draw_47045.cljs$core$IFn$_invoke$arity$2(G__47035_47049,G__47036_47050) : draw_47045.call(null,G__47035_47049,G__47036_47050));
}catch (e47034){if((e47034 instanceof Error)){
var e_47051 = e47034;
console.log(e_47051);
} else {
throw e47034;

}
}} else {
}

var G__47052 = (i_47040 + (1));
i_47040 = G__47052;
continue;
} else {
}
break;
}

var G__47037 = ((function (map__47028,map__47028__$1,mc,canvas,updating_QMARK_,ctx,active,entities){
return (function (){
return monet$canvas$draw_loop(mc);
});})(map__47028,map__47028__$1,mc,canvas,updating_QMARK_,ctx,active,entities))
;
return (monet.core.animation_frame.cljs$core$IFn$_invoke$arity$1 ? monet.core.animation_frame.cljs$core$IFn$_invoke$arity$1(G__47037) : monet.core.animation_frame.call(null,G__47037));
} else {
return null;
}
});
monet.canvas.monet_canvas = (function monet$canvas$monet_canvas(elem,context_type){
var ct = (function (){var or__6153__auto__ = context_type;
if(cljs.core.truth_(or__6153__auto__)){
return or__6153__auto__;
} else {
return "2d";
}
})();
var ctx = monet.canvas.get_context(elem,ct);
return new cljs.core.PersistentArrayMap(null, 5, [cljs.core.cst$kw$canvas,elem,cljs.core.cst$kw$ctx,ctx,cljs.core.cst$kw$entities,{},cljs.core.cst$kw$updating_QMARK_,(cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(true) : cljs.core.atom.call(null,true)),cljs.core.cst$kw$active,(cljs.core.atom.cljs$core$IFn$_invoke$arity$1 ? cljs.core.atom.cljs$core$IFn$_invoke$arity$1(true) : cljs.core.atom.call(null,true))], null);
});
monet.canvas.init = (function monet$canvas$init(var_args){
var args__7218__auto__ = [];
var len__7211__auto___47061 = arguments.length;
var i__7212__auto___47062 = (0);
while(true){
if((i__7212__auto___47062 < len__7211__auto___47061)){
args__7218__auto__.push((arguments[i__7212__auto___47062]));

var G__47063 = (i__7212__auto___47062 + (1));
i__7212__auto___47062 = G__47063;
continue;
} else {
}
break;
}

var argseq__7219__auto__ = ((((1) < args__7218__auto__.length))?(new cljs.core.IndexedSeq(args__7218__auto__.slice((1)),(0))):null);
return monet.canvas.init.cljs$core$IFn$_invoke$arity$variadic((arguments[(0)]),argseq__7219__auto__);
});

monet.canvas.init.cljs$core$IFn$_invoke$arity$variadic = (function (canvas,p__47059){
var vec__47060 = p__47059;
var context_type = cljs.core.nth.cljs$core$IFn$_invoke$arity$3(vec__47060,(0),null);
var mc = monet.canvas.monet_canvas(canvas,context_type);
monet.canvas.draw_loop(mc);

return mc;
});

monet.canvas.init.cljs$lang$maxFixedArity = (1);

monet.canvas.init.cljs$lang$applyTo = (function (seq47057){
var G__47058 = cljs.core.first(seq47057);
var seq47057__$1 = cljs.core.next(seq47057);
return monet.canvas.init.cljs$core$IFn$_invoke$arity$variadic(G__47058,seq47057__$1);
});
monet.canvas.stop = (function monet$canvas$stop(mc){
var G__47066 = cljs.core.cst$kw$active.cljs$core$IFn$_invoke$arity$1(mc);
var G__47067 = false;
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__47066,G__47067) : cljs.core.reset_BANG_.call(null,G__47066,G__47067));
});
monet.canvas.stop_updating = (function monet$canvas$stop_updating(mc){
var G__47070 = cljs.core.cst$kw$updating_QMARK_.cljs$core$IFn$_invoke$arity$1(mc);
var G__47071 = false;
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__47070,G__47071) : cljs.core.reset_BANG_.call(null,G__47070,G__47071));
});
monet.canvas.start_updating = (function monet$canvas$start_updating(mc){
var G__47074 = cljs.core.cst$kw$updating_QMARK_.cljs$core$IFn$_invoke$arity$1(mc);
var G__47075 = true;
return (cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__47074,G__47075) : cljs.core.reset_BANG_.call(null,G__47074,G__47075));
});
monet.canvas.restart = (function monet$canvas$restart(mc){
var G__47078_47080 = cljs.core.cst$kw$active.cljs$core$IFn$_invoke$arity$1(mc);
var G__47079_47081 = true;
(cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2 ? cljs.core.reset_BANG_.cljs$core$IFn$_invoke$arity$2(G__47078_47080,G__47079_47081) : cljs.core.reset_BANG_.call(null,G__47078_47080,G__47079_47081));

return monet.canvas.draw_loop(mc);
});
