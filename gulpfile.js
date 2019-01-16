'use strict';

const 	gulp = require('gulp'),
		sass = require('gulp-sass'),
		babel = require('gulp-babel'),
		concat = require('gulp-concat'),
		uglify = require('gulp-uglify'),
		rename = require('gulp-rename'),
		cleanCSS = require('gulp-clean-css'),
		del = require('del'),
		imagemin = require("gulp-imagemin"),
		browsersync = require('browser-sync'),
		server = browsersync.create();

const paths = {
  styles: {
    src: 'src/scss/**/*.scss',
    msrc: 'src/scss/main.scss',
    dest: 'public/static/css/'
  },
  scripts: {
    src: 'src/js/**/*.js',
    dest: 'public/static/js/'
  },
  images: {
    src: 'src/img/**/*.{jpg,jpeg,png,svg}',
    dest: 'public/static/img/'
  }
};

// Tasks
function styles() {
  return gulp.src(paths.styles.src)
    .pipe(sass())
    .pipe(gulp.dest(paths.styles.dest))
    .pipe(cleanCSS())
    // pass in options to the stream
    .pipe(rename({
      basename: 'main',
      suffix: '.min'
    }))
    .pipe(gulp.dest(paths.styles.dest));
}

function clean() {
  return del([ './public/static' ]);
}

function scripts() {
  return gulp.src(paths.scripts.src, { sourcemaps: true })
    .pipe(babel())
    .pipe(gulp.dest(paths.scripts.dest))
    .pipe(uglify())
    .pipe(concat('main.min.js'))
    .pipe(gulp.dest(paths.scripts.dest));
}

function images() {
  return gulp.src(paths.images.src, {since: gulp.lastRun(images)})
    .pipe(imagemin({optimizationLevel: 5}))
    .pipe(gulp.dest(paths.images.dest));
}

function fonts() {
  return gulp.src('src/fonts/**/*')
        .pipe(gulp.dest('public/static/fonts'))
}

function vendor() {
  return gulp.src('src/vendor/**/*')
        .pipe(gulp.dest('public/static/vendor'))
}

function watch() {
  gulp.watch(paths.scripts.src, gulp.series(scripts));
  gulp.watch(paths.styles.src, gulp.series(styles));
  gulp.watch(paths.images.src, gulp.series(images));
}

gulp.task('default', gulp.series(
  clean, 
  gulp.parallel(
    scripts, 
    styles, 
    images,
    fonts,
    vendor,
  ),
  watch
));