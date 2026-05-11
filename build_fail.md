build(Linux, arm64, ubuntu-24.04-arm)
… … 


98:17.93 1004 |     pub(crate) fn iter(&self) -> ClangTokenIterator<'_> {
98:17.93      |                                                    ++++
98:17.93 warning: hiding a lifetime that's elided elsewhere is confusing
98:17.93     --> third_party/rust/bindgen/ir/context.rs:1243:9
98:17.93      |
98:17.93 1243 |         &self,
98:17.93      |         ^^^^^ the lifetime is elided here
98:17.93 1244 |     ) -> traversal::AssertNoDanglingItemsTraversal {
98:17.93      |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ the same lifetime is hidden here
98:17.94      |
98:17.94      = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:17.94 help: use `'_` for type paths
98:17.94      |
98:17.94 1244 |     ) -> traversal::AssertNoDanglingItemsTraversal<'_> {
98:17.94      |                                                   ++++
98:17.94 warning: hiding a lifetime that's elided elsewhere is confusing
98:17.94    --> third_party/rust/bindgen/ir/ty.rs:246:28
98:17.94     |
98:17.94 246 |     fn sanitize_name(name: &str) -> Cow<str> {
98:17.94     |                            ^^^^     ^^^^^^^^ the same lifetime is hidden here
98:17.94     |                            |
98:17.94     |                            the lifetime is elided here
98:17.94     |
98:17.94     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:17.94 help: use `'_` for type paths
98:17.94     |
98:17.94 246 |     fn sanitize_name(name: &str) -> Cow<'_, str> {
98:17.94     |                                         +++
98:17.94 warning: `bindgen` (lib) generated 6 warnings (run `cargo fix --lib -p bindgen` to apply 5 suggestions)
98:17.94    Compiling builtins-static v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/builtins)
98:18.43 warning: unexpected `cfg` condition value: `testlib`
98:18.43    --> security/manager/ssl/builtins/build.rs:351:11
98:18.43     |
98:18.43 351 |     #[cfg(feature = "testlib")]
98:18.43     |           ^^^^^^^^^^^^^^^^^^^
98:18.43     |
98:18.43     = note: expected values for `feature` are: `mozilla-central-workspace-hack`
98:18.43     = help: consider adding `testlib` as a feature in `Cargo.toml`
98:18.43     = note: see <https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html> for more information about checking conditional configuration
98:18.43     = note: `#[warn(unexpected_cfgs)]` on by default
98:18.43 warning: unexpected `cfg` condition value: `testlib`
98:18.43    --> security/manager/ssl/builtins/build.rs:356:15
98:18.43     |
98:18.43 356 |     #[cfg(not(feature = "testlib"))]
98:18.43     |               ^^^^^^^^^^^^^^^^^^^
98:18.43     |
98:18.43     = note: expected values for `feature` are: `mozilla-central-workspace-hack`
98:18.43     = help: consider adding `testlib` as a feature in `Cargo.toml`
98:18.43     = note: see <https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html> for more information about checking conditional configuration
98:18.85 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.85    --> security/manager/ssl/builtins/build.rs:101:13
98:18.85     |
98:18.85 101 | fn class(i: &str) -> IResult<&str, Ck> {
98:18.85     |             ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.85     |             |                |
98:18.85     |             |                the same lifetime is elided here
98:18.85     |             the lifetime is elided here
98:18.85     |
98:18.85     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.85     = note: `#[warn(mismatched_lifetime_syntaxes)]` on by default
98:18.85 help: use `'_` for type paths
98:18.85     |
98:18.85 101 | fn class(i: &str) -> IResult<&str, Ck<'_>> {
98:18.85     |                                      ++++
98:18.85 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.85    --> security/manager/ssl/builtins/build.rs:114:13
98:18.85     |
98:18.85 114 | fn trust(i: &str) -> IResult<&str, Ck> {
98:18.85     |             ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.85     |             |                |
98:18.85     |             |                the same lifetime is elided here
98:18.85     |             the lifetime is elided here
98:18.86     |
98:18.86     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.86 help: use `'_` for type paths
98:18.86     |
98:18.86 114 | fn trust(i: &str) -> IResult<&str, Ck<'_>> {
98:18.86     |                                      ++++
98:18.86 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.86    --> security/manager/ssl/builtins/build.rs:129:20
98:18.86     |
98:18.86 129 | fn option_bbool(i: &str) -> IResult<&str, Ck> {
98:18.86     |                    ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.86     |                    |                |
98:18.86     |                    |                the same lifetime is elided here
98:18.86     |                    the lifetime is elided here
98:18.86     |
98:18.86     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.86 help: use `'_` for type paths
98:18.86     |
98:18.86 129 | fn option_bbool(i: &str) -> IResult<&str, Ck<'_>> {
98:18.86     |                                             ++++
98:18.86 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.86    --> security/manager/ssl/builtins/build.rs:138:18
98:18.86     |
98:18.86 138 | fn bbool_true(i: &str) -> IResult<&str, Ck> {
98:18.86     |                  ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.86     |                  |                |
98:18.86     |                  |                the same lifetime is elided here
98:18.86     |                  the lifetime is elided here
98:18.86     |
98:18.86     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.86 help: use `'_` for type paths
98:18.86     |
98:18.86 138 | fn bbool_true(i: &str) -> IResult<&str, Ck<'_>> {
98:18.86     |                                           ++++
98:18.86 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.86    --> security/manager/ssl/builtins/build.rs:147:19
98:18.87     |
98:18.87 147 | fn bbool_false(i: &str) -> IResult<&str, Ck> {
98:18.87     |                   ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.87     |                   |                |
98:18.87     |                   |                the same lifetime is elided here
98:18.87     |                   the lifetime is elided here
98:18.87     |
98:18.87     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.87 help: use `'_` for type paths
98:18.87     |
98:18.87 147 | fn bbool_false(i: &str) -> IResult<&str, Ck<'_>> {
98:18.87     |                                            ++++
98:18.87 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.87    --> security/manager/ssl/builtins/build.rs:156:12
98:18.87     |
98:18.87 156 | fn utf8(i: &str) -> IResult<&str, Ck> {
98:18.87     |            ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.87     |            |                |
98:18.87     |            |                the same lifetime is elided here
98:18.87     |            the lifetime is elided here
98:18.87     |
98:18.87     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.87 help: use `'_` for type paths
98:18.87     |
98:18.87 156 | fn utf8(i: &str) -> IResult<&str, Ck<'_>> {
98:18.87     |                                     ++++
98:18.87 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.87    --> security/manager/ssl/builtins/build.rs:167:24
98:18.87     |
98:18.87 167 | fn certificate_type(i: &str) -> IResult<&str, Ck> {
98:18.87     |                        ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.87     |                        |                |
98:18.87     |                        |                the same lifetime is elided here
98:18.87     |                        the lifetime is elided here
98:18.87     |
98:18.87     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.87 help: use `'_` for type paths
98:18.87     |
98:18.87 167 | fn certificate_type(i: &str) -> IResult<&str, Ck<'_>> {
98:18.87     |                                                 ++++
98:18.87 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.87    --> security/manager/ssl/builtins/build.rs:178:22
98:18.87     |
98:18.87 178 | fn distrust_after(i: &str) -> IResult<&str, Ck> {
98:18.88     |                      ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.88     |                      |                |
98:18.88     |                      |                the same lifetime is elided here
98:18.88     |                      the lifetime is elided here
98:18.88     |
98:18.88     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.88 help: use `'_` for type paths
98:18.88     |
98:18.88 178 | fn distrust_after(i: &str) -> IResult<&str, Ck<'_>> {
98:18.88     |                                               ++++
98:18.88 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.88    --> security/manager/ssl/builtins/build.rs:196:23
98:18.88     |
98:18.88 196 | fn multiline_octal(i: &str) -> IResult<&str, Ck> {
98:18.88     |                       ^^^^             ^^^^  ^^ the same lifetime is hidden here
98:18.88     |                       |                |
98:18.88     |                       |                the same lifetime is elided here
98:18.88     |                       the lifetime is elided here
98:18.88     |
98:18.88     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.88 help: use `'_` for type paths
98:18.88     |
98:18.88 196 | fn multiline_octal(i: &str) -> IResult<&str, Ck<'_>> {
98:18.88     |                                                ++++
98:18.88 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.88    --> security/manager/ssl/builtins/build.rs:207:24
98:18.88     |
98:18.88 207 | fn distrust_comment(i: &str) -> IResult<&str, (&str, Ck)> {
98:18.88     |                        ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
98:18.88     |                        |                |      |
98:18.88     |                        |                |      the same lifetime is elided here
98:18.88     |                        |                the same lifetime is elided here
98:18.88     |                        the lifetime is elided here
98:18.88     |
98:18.88     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.88 help: use `'_` for type paths
98:18.88     |
98:18.88 207 | fn distrust_comment(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
98:18.88     |                                                        ++++
98:18.88 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.88    --> security/manager/ssl/builtins/build.rs:219:15
98:18.88     |
98:18.88 219 | fn comment(i: &str) -> IResult<&str, (&str, Ck)> {
98:18.88     |               ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
98:18.88     |               |                |      |
98:18.88     |               |                |      the same lifetime is elided here
98:18.88     |               |                the same lifetime is elided here
98:18.88     |               the lifetime is elided here
98:18.88     |
98:18.88     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.88 help: use `'_` for type paths
98:18.88     |
98:18.88 219 | fn comment(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
98:18.88     |                                               ++++
98:18.88 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.88    --> security/manager/ssl/builtins/build.rs:224:21
98:18.88     |
98:18.88 224 | fn certdata_line(i: &str) -> IResult<&str, (&str, Ck)> {
98:18.88     |                     ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
98:18.88     |                     |                |      |
98:18.88     |                     |                |      the same lifetime is elided here
98:18.88     |                     |                the same lifetime is elided here
98:18.88     |                     the lifetime is elided here
98:18.88     |
98:18.88     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.88 help: use `'_` for type paths
98:18.88     |
98:18.89 224 | fn certdata_line(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
98:18.89     |                                                     ++++
98:18.89 warning: hiding a lifetime that's elided elsewhere is confusing
98:18.89    --> security/manager/ssl/builtins/build.rs:281:13
98:18.89     |
98:18.89 281 | fn parse(i: &str) -> IResult<&str, Vec<Block>> {
98:18.89     |             ^^^^             ^^^^      ^^^^^ the same lifetime is hidden here
98:18.89     |             |                |
98:18.89     |             |                the same lifetime is elided here
98:18.89     |             the lifetime is elided here
98:18.89     |
98:18.89     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
98:18.89 help: use `'_` for type paths
98:18.89     |
98:18.89 281 | fn parse(i: &str) -> IResult<&str, Vec<Block<'_>>> {
98:18.89     |                                             ++++
98:21.94 warning: `builtins-static` (build script) generated 15 warnings
98:21.94    Compiling mozilla-central-workspace-hack v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/build/workspace-hack)
98:28.83     Finished `release` profile [optimized] target(s) in 15.20s
98:30.06 security/manager/ssl/builtins/libbuiltins_static.a
98:30.07 js/src/gc
98:37.13 layout/style
99:01.64 media/libdav1d
99:02.70 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/third_party/dav1d/src/cpu.c:110:9: warning: code will never be executed [-Wunreachable-code]
99:02.70   110 |     if (c)
99:02.70       |         ^
99:02.70 1 warning generated.
99:36.43 netwerk/base
100:15.18 netwerk/dns
101:55.40 security/manager/ssl
102:23.50 toolkit/components/telemetry
102:36.94 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
102:36.94 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
102:36.94 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:91:11: error: redefinition of 'end' with a different type: 'char *' vs 'size_t' (aka 'unsigned long')
102:36.94    91 |     char* end = nullptr;
102:36.94       |           ^
102:36.94 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:83:12: note: previous definition is here
102:36.94    83 |     size_t end = token.find_last_not_of(" \t");
102:36.94       |            ^
102:36.94 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:92:53: error: cannot initialize a parameter of type 'char **' with an rvalue of type 'size_t *' (aka 'unsigned long *')
102:36.94    92 |     unsigned long val = std::strtoul(token.c_str(), &end, 16);
102:36.94       |                                                     ^~~~
102:36.94 /usr/include/stdlib.h:221:26: note: passing argument to parameter '__endptr' here
102:36.94   221 |                                           char **__restrict __endptr,
102:36.94       |                                                             ^
102:36.94 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
102:36.94 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
102:36.94 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:27: error: comparison between pointer and integer ('size_t' (aka 'unsigned long') and 'const char *')
102:36.94    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
102:36.94       |                       ~~~ ^  ~~~~~~~~~~~~~
102:36.94 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:47: error: indirection requires pointer operand ('size_t' (aka 'unsigned long') invalid)
102:36.94    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
102:36.94       |                                               ^~~~
102:51.00 4 errors generated.
102:51.09 gmake[5]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:676: Unified_cpp_security_manager_ssl2.o] Error 1
102:51.09 gmake[5]: *** Waiting for unfinished jobs....
102:57.90 toolkit/library/buildid.cpp.stub
102:58.16 toolkit/library
103:00.85 gmake[4]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:72: security/manager/ssl/target-objects] Error 2
103:00.85 gmake[4]: *** Waiting for unfinished jobs....
105:09.62 gmake[3]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:34: compile] Error 2
105:09.67 gmake[2]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:359: default] Error 2
105:09.72 gmake[1]: *** [client.mk:60: build] Error 2
105:09.82 W 240 compiler warnings present.
105:11.79 W Notification center failed: Install notify-send (usually part of the libnotify package) to get a notification when the build finishes.
 Config object not found by mach.
Configure complete!
Be sure to run |mach build| to pick up any changes
  Parallelism determined by memory: using 4 jobs for 4 cores based on 15.6 GiB RAM and estimated job size of 1.0 GiB
make: *** [Makefile:132: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.
build (linux, arm64, ubuntu-24.04-arm)

……53:55.52  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:55.52       |                                     ^
53:55.52 In file included from Unified_cpp_widget_gtk2.cpp:83:
53:55.52 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsFilePicker.cpp:713:63: warning: 'GtkStock' is deprecated [-Wdeprecated-declarations]
53:55.52   713 |                                                             : GTK_STOCK_OPEN;
53:55.52       |                                                               ^
53:55.52 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:765:38: note: expanded from macro 'GTK_STOCK_OPEN'
53:55.52   765 | #define GTK_STOCK_OPEN             ((GtkStock)"gtk-open")
53:55.52       |                                      ^
53:55.52 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:105:1: note: 'GtkStock' has been explicitly marked deprecated here
53:55.52   105 | G_DEPRECATED
53:55.52       | ^
53:55.52 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:55.52  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:55.52       |                                     ^
53:55.52 In file included from Unified_cpp_widget_gtk2.cpp:83:
53:55.52 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsFilePicker.cpp:716:30: warning: 'GtkStock' is deprecated [-Wdeprecated-declarations]
53:55.52   716 |       title, parent, action, GTK_STOCK_CANCEL, GTK_RESPONSE_CANCEL,
53:55.52       |                              ^
53:55.52 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:159:38: note: expanded from macro 'GTK_STOCK_CANCEL'
53:55.52   159 | #define GTK_STOCK_CANCEL           ((GtkStock)"gtk-cancel")
53:55.52       |                                      ^
53:55.52 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:105:1: note: 'GtkStock' has been explicitly marked deprecated here
53:55.52   105 | G_DEPRECATED
53:55.52       | ^
53:55.52 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:55.52  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:55.52       |                                     ^
53:55.52 In file included from Unified_cpp_widget_gtk2.cpp:83:
53:55.52 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsFilePicker.cpp:718:3: warning: 'gtk_dialog_set_alternative_button_order' is deprecated [-Wdeprecated-declarations]
53:55.52   718 |   gtk_dialog_set_alternative_button_order(
53:55.52       |   ^
53:55.52 /usr/include/gtk-3.0/gtk/gtkdialog.h:184:1: note: 'gtk_dialog_set_alternative_button_order' has been explicitly marked deprecated here
53:55.52   184 | GDK_DEPRECATED_IN_3_10
53:55.52       | ^
53:55.52 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:328:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_10'
53:55.52   328 | # define GDK_DEPRECATED_IN_3_10               GDK_DEPRECATED
53:55.52       |                                               ^
53:55.52 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:55.52    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:55.52       |                        ^
53:55.52 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:55.52  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:55.52       |                                     ^
53:55.88 xpcom/base
53:58.48 In file included from Unified_cpp_widget_gtk2.cpp:110:
53:58.48 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsLookAndFeel.cpp:512:8: warning: 'gtk_style_properties_lookup_property' is deprecated [-Wdeprecated-declarations]
53:58.48   512 |   if (!gtk_style_properties_lookup_property(propertyName, nullptr, nullptr))
53:58.48       |        ^
53:58.48 /usr/include/gtk-3.0/gtk/deprecated/gtkstyleproperties.h:75:1: note: 'gtk_style_properties_lookup_property' has been explicitly marked deprecated here
53:58.48    75 | GDK_DEPRECATED_IN_3_8
53:58.48       | ^
53:58.48 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:314:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_8'
53:58.48   314 | # define GDK_DEPRECATED_IN_3_8                GDK_DEPRECATED
53:58.48       |                                               ^
53:58.48 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.48    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.48       |                        ^
53:58.48 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.48  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.48       |                                     ^
53:58.53 In file included from Unified_cpp_widget_gtk2.cpp:110:
53:58.53 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsLookAndFeel.cpp:2287:3: warning: 'gtk_style_context_add_region' is deprecated [-Wdeprecated-declarations]
53:58.53  2287 |   gtk_style_context_add_region(style, GTK_STYLE_REGION_ROW, GTK_REGION_ODD);
53:58.53       |   ^
53:58.53 /usr/include/gtk-3.0/gtk/gtkstylecontext.h:1107:1: note: 'gtk_style_context_add_region' has been explicitly marked deprecated here
53:58.53  1107 | GDK_DEPRECATED_IN_3_14
53:58.53       | ^
53:58.53 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:356:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_14'
53:58.53   356 | # define GDK_DEPRECATED_IN_3_14               GDK_DEPRECATED
53:58.53       |                                               ^
53:58.53 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.53    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.53       |                        ^
53:58.53 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.53  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.53       |                                     ^
53:58.55 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:74:43: warning: 'GtkStock' is deprecated [-Wdeprecated-declarations]
53:58.56    74 |       (GtkDialogFlags)(GTK_DIALOG_MODAL), GTK_STOCK_CANCEL, GTK_RESPONSE_REJECT,
53:58.56       |                                           ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:159:38: note: expanded from macro 'GTK_STOCK_CANCEL'
53:58.56   159 | #define GTK_STOCK_CANCEL           ((GtkStock)"gtk-cancel")
53:58.56       |                                      ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:105:1: note: 'GtkStock' has been explicitly marked deprecated here
53:58.56   105 | G_DEPRECATED
53:58.56       | ^
53:58.56 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.56  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.56       |                                     ^
53:58.56 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:75:7: warning: 'GtkStock' is deprecated [-Wdeprecated-declarations]
53:58.56    75 |       GTK_STOCK_OK, GTK_RESPONSE_ACCEPT, nullptr);
53:58.56       |       ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:756:38: note: expanded from macro 'GTK_STOCK_OK'
53:58.56   756 | #define GTK_STOCK_OK               ((GtkStock)"gtk-ok")
53:58.56       |                                      ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:105:1: note: 'GtkStock' has been explicitly marked deprecated here
53:58.56   105 | G_DEPRECATED
53:58.56       | ^
53:58.56 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.56  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.56       |                                     ^
53:58.56 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:78:3: warning: 'gtk_dialog_set_alternative_button_order' is deprecated [-Wdeprecated-declarations]
53:58.56    78 |   gtk_dialog_set_alternative_button_order(
53:58.56       |   ^
53:58.56 /usr/include/gtk-3.0/gtk/gtkdialog.h:184:1: note: 'gtk_dialog_set_alternative_button_order' has been explicitly marked deprecated here
53:58.56   184 | GDK_DEPRECATED_IN_3_10
53:58.56       | ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:328:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_10'
53:58.56   328 | # define GDK_DEPRECATED_IN_3_10               GDK_DEPRECATED
53:58.56       |                                               ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.56    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.56       |                        ^
53:58.56 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.56  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.56       |                                     ^
53:58.56 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:86:32: warning: 'GtkStock' is deprecated [-Wdeprecated-declarations]
53:58.56    86 |       gtk_image_new_from_stock(GTK_STOCK_DIALOG_QUESTION, GTK_ICON_SIZE_DIALOG);
53:58.56       |                                ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:302:38: note: expanded from macro 'GTK_STOCK_DIALOG_QUESTION'
53:58.56   302 | #define GTK_STOCK_DIALOG_QUESTION  ((GtkStock)"gtk-dialog-question")
53:58.56       |                                      ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkstock.h:105:1: note: 'GtkStock' has been explicitly marked deprecated here
53:58.56   105 | G_DEPRECATED
53:58.56       | ^
53:58.56 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.56  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.56       |                                     ^
53:58.56 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:86:7: warning: 'gtk_image_new_from_stock' is deprecated: Use 'gtk_image_new_from_icon_name' instead [-Wdeprecated-declarations]
53:58.56    86 |       gtk_image_new_from_stock(GTK_STOCK_DIALOG_QUESTION, GTK_ICON_SIZE_DIALOG);
53:58.56       |       ^
53:58.56 /usr/include/gtk-3.0/gtk/gtkimage.h:121:1: note: 'gtk_image_new_from_stock' has been explicitly marked deprecated here
53:58.56   121 | GDK_DEPRECATED_IN_3_10_FOR(gtk_image_new_from_icon_name)
53:58.56       | ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:329:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_10_FOR'
53:58.56   329 | # define GDK_DEPRECATED_IN_3_10_FOR(f)        GDK_DEPRECATED_FOR(f)
53:58.56       |                                               ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.56    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.56       |                               ^
53:58.56 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.56  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.56       |                                            ^
53:58.56 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:98:28: warning: 'gtk_vbox_new' is deprecated: Use 'gtk_box_new' instead [-Wdeprecated-declarations]
53:58.56    98 |   GtkWidget* custom_vbox = gtk_vbox_new(TRUE, 2);
53:58.56       |                            ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkvbox.h:60:1: note: 'gtk_vbox_new' has been explicitly marked deprecated here
53:58.56    60 | GDK_DEPRECATED_IN_3_2_FOR(gtk_box_new)
53:58.56       | ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:273:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_2_FOR'
53:58.56   273 | # define GDK_DEPRECATED_IN_3_2_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.56       |                                               ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.56    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.56       |                               ^
53:58.56 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.56  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.56       |                                            ^
53:58.56 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:102:28: warning: 'gtk_hbox_new' is deprecated: Use 'gtk_box_new' instead [-Wdeprecated-declarations]
53:58.56   102 |   GtkWidget* custom_hbox = gtk_hbox_new(FALSE, 2);
53:58.56       |                            ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkhbox.h:62:1: note: 'gtk_hbox_new' has been explicitly marked deprecated here
53:58.56    62 | GDK_DEPRECATED_IN_3_2_FOR(gtk_box_new)
53:58.56       | ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:273:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_2_FOR'
53:58.56   273 | # define GDK_DEPRECATED_IN_3_2_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.56       |                                               ^
53:58.56 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.56    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.56       |                               ^
53:58.56 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.56  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.56       |                                            ^
53:58.56 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.56 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:191:35: warning: 'gtk_vbox_new' is deprecated: Use 'gtk_box_new' instead [-Wdeprecated-declarations]
53:58.56   191 |   GtkWidget* custom_options_tab = gtk_vbox_new(FALSE, 0);
53:58.56       |                                   ^
53:58.56 /usr/include/gtk-3.0/gtk/deprecated/gtkvbox.h:60:1: note: 'gtk_vbox_new' has been explicitly marked deprecated here
53:58.57    60 | GDK_DEPRECATED_IN_3_2_FOR(gtk_box_new)
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:273:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_2_FOR'
53:58.57   273 | # define GDK_DEPRECATED_IN_3_2_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.57    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.57       |                               ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.57  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.57       |                                            ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:197:40: warning: 'gtk_vbox_new' is deprecated: Use 'gtk_box_new' instead [-Wdeprecated-declarations]
53:58.57   197 |   GtkWidget* check_buttons_container = gtk_vbox_new(TRUE, 2);
53:58.57       |                                        ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkvbox.h:60:1: note: 'gtk_vbox_new' has been explicitly marked deprecated here
53:58.57    60 | GDK_DEPRECATED_IN_3_2_FOR(gtk_box_new)
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:273:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_2_FOR'
53:58.57   273 | # define GDK_DEPRECATED_IN_3_2_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.57    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.57       |                               ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.57  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.57       |                                            ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:221:45: warning: 'gtk_vbox_new' is deprecated: Use 'gtk_box_new' instead [-Wdeprecated-declarations]
53:58.57   221 |   GtkWidget* appearance_buttons_container = gtk_vbox_new(TRUE, 2);
53:58.57       |                                             ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkvbox.h:60:1: note: 'gtk_vbox_new' has been explicitly marked deprecated here
53:58.57    60 | GDK_DEPRECATED_IN_3_2_FOR(gtk_box_new)
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:273:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_2_FOR'
53:58.57   273 | # define GDK_DEPRECATED_IN_3_2_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.57    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.57       |                               ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.57  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.57       |                                            ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:237:3: warning: 'gtk_misc_set_alignment' is deprecated [-Wdeprecated-declarations]
53:58.57   237 |   gtk_misc_set_alignment(GTK_MISC(appearance_label), 0, 0);
53:58.57       |   ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkmisc.h:71:1: note: 'gtk_misc_set_alignment' has been explicitly marked deprecated here
53:58.57    71 | GDK_DEPRECATED_IN_3_14
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:356:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_14'
53:58.57   356 | # define GDK_DEPRECATED_IN_3_14               GDK_DEPRECATED
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.57    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.57       |                        ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.57  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.57       |                                     ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:239:37: warning: 'gtk_alignment_new' is deprecated [-Wdeprecated-declarations]
53:58.57   239 |   GtkWidget* appearance_container = gtk_alignment_new(0, 0, 0, 0);
53:58.57       |                                     ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkalignment.h:78:1: note: 'gtk_alignment_new' has been explicitly marked deprecated here
53:58.57    78 | GDK_DEPRECATED_IN_3_14
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:356:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_14'
53:58.57   356 | # define GDK_DEPRECATED_IN_3_14               GDK_DEPRECATED
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.57    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.57       |                        ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.57  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.57       |                                     ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:240:3: warning: 'gtk_alignment_set_padding' is deprecated [-Wdeprecated-declarations]
53:58.57   240 |   gtk_alignment_set_padding(GTK_ALIGNMENT(appearance_container), 8, 0, 12, 0);
53:58.57       |   ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkalignment.h:90:1: note: 'gtk_alignment_set_padding' has been explicitly marked deprecated here
53:58.57    90 | GDK_DEPRECATED_IN_3_14
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:356:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_14'
53:58.57   356 | # define GDK_DEPRECATED_IN_3_14               GDK_DEPRECATED
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.57    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.57       |                        ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.57  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.57       |                                     ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:244:45: warning: 'gtk_vbox_new' is deprecated: Use 'gtk_box_new' instead [-Wdeprecated-declarations]
53:58.57   244 |   GtkWidget* appearance_vertical_squasher = gtk_vbox_new(FALSE, 0);
53:58.57       |                                             ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkvbox.h:60:1: note: 'gtk_vbox_new' has been explicitly marked deprecated here
53:58.57    60 | GDK_DEPRECATED_IN_3_2_FOR(gtk_box_new)
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:273:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_2_FOR'
53:58.57   273 | # define GDK_DEPRECATED_IN_3_2_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.57    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.57       |                               ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.57  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.57       |                                            ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:256:3: warning: 'gtk_misc_set_alignment' is deprecated [-Wdeprecated-declarations]
53:58.57   256 |   gtk_misc_set_alignment(GTK_MISC(header_footer_label), 0, 0);
53:58.57       |   ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkmisc.h:71:1: note: 'gtk_misc_set_alignment' has been explicitly marked deprecated here
53:58.57    71 | GDK_DEPRECATED_IN_3_14
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:356:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_14'
53:58.57   356 | # define GDK_DEPRECATED_IN_3_14               GDK_DEPRECATED
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.57    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.57       |                        ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.57  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.57       |                                     ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:258:40: warning: 'gtk_alignment_new' is deprecated [-Wdeprecated-declarations]
53:58.57   258 |   GtkWidget* header_footer_container = gtk_alignment_new(0, 0, 0, 0);
53:58.57       |                                        ^
53:58.57 /usr/include/gtk-3.0/gtk/deprecated/gtkalignment.h:78:1: note: 'gtk_alignment_new' has been explicitly marked deprecated here
53:58.57    78 | GDK_DEPRECATED_IN_3_14
53:58.57       | ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:356:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_14'
53:58.57   356 | # define GDK_DEPRECATED_IN_3_14               GDK_DEPRECATED
53:58.57       |                                               ^
53:58.57 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.57    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.57       |                        ^
53:58.57 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.57  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.57       |                                     ^
53:58.57 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.58 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:259:3: warning: 'gtk_alignment_set_padding' is deprecated [-Wdeprecated-declarations]
53:58.58   259 |   gtk_alignment_set_padding(GTK_ALIGNMENT(header_footer_container), 8, 0, 12,
53:58.58       |   ^
53:58.58 /usr/include/gtk-3.0/gtk/deprecated/gtkalignment.h:90:1: note: 'gtk_alignment_set_padding' has been explicitly marked deprecated here
53:58.58    90 | GDK_DEPRECATED_IN_3_14
53:58.58       | ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:356:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_14'
53:58.58   356 | # define GDK_DEPRECATED_IN_3_14               GDK_DEPRECATED
53:58.58       |                                               ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:48:24: note: expanded from macro 'GDK_DEPRECATED'
53:58.58    48 | #define GDK_DEPRECATED G_DEPRECATED _GDK_EXTERN
53:58.58       |                        ^
53:58.58 /usr/include/glib-2.0/glib/gmacros.h:1263:37: note: expanded from macro 'G_DEPRECATED'
53:58.58  1263 | #define G_DEPRECATED __attribute__((__deprecated__))
53:58.58       |                                     ^
53:58.58 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.58 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:263:36: warning: 'gtk_table_new' is deprecated: Use 'GtkGrid' instead [-Wdeprecated-declarations]
53:58.58   263 |   GtkWidget* header_footer_table = gtk_table_new(3, 3, FALSE);  // 3x3 table
53:58.58       |                                    ^
53:58.58 /usr/include/gtk-3.0/gtk/deprecated/gtktable.h:118:1: note: 'gtk_table_new' has been explicitly marked deprecated here
53:58.58   118 | GDK_DEPRECATED_IN_3_4_FOR(GtkGrid)
53:58.58       | ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:287:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_4_FOR'
53:58.58   287 | # define GDK_DEPRECATED_IN_3_4_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.58       |                                               ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.58    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.58       |                               ^
53:58.58 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.58  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.58       |                                            ^
53:58.58 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.58 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:275:5: warning: 'gtk_table_attach' is deprecated: Use 'GtkGrid' instead [-Wdeprecated-declarations]
53:58.58   275 |     gtk_table_attach(GTK_TABLE(header_footer_table), header_dropdown[i], i,
53:58.58       |     ^
53:58.58 /usr/include/gtk-3.0/gtk/deprecated/gtktable.h:126:1: note: 'gtk_table_attach' has been explicitly marked deprecated here
53:58.58   126 | GDK_DEPRECATED_IN_3_4_FOR(GtkGrid)
53:58.58       | ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:287:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_4_FOR'
53:58.58   287 | # define GDK_DEPRECATED_IN_3_4_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.58       |                                               ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.58    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.58       |                               ^
53:58.58 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.58  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.58       |                                            ^
53:58.58 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.58 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:282:5: warning: 'gtk_table_attach' is deprecated: Use 'GtkGrid' instead [-Wdeprecated-declarations]
53:58.58   282 |     gtk_table_attach(GTK_TABLE(header_footer_table),
53:58.58       |     ^
53:58.58 /usr/include/gtk-3.0/gtk/deprecated/gtktable.h:126:1: note: 'gtk_table_attach' has been explicitly marked deprecated here
53:58.58   126 | GDK_DEPRECATED_IN_3_4_FOR(GtkGrid)
53:58.58       | ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:287:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_4_FOR'
53:58.58   287 | # define GDK_DEPRECATED_IN_3_4_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.58       |                                               ^
53:58.58 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.58    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.59       |                               ^
53:58.59 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.59  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.59       |                                            ^
53:58.59 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.59 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:295:5: warning: 'gtk_table_attach' is deprecated: Use 'GtkGrid' instead [-Wdeprecated-declarations]
53:58.59   295 |     gtk_table_attach(GTK_TABLE(header_footer_table), footer_dropdown[i], i,
53:58.59       |     ^
53:58.59 /usr/include/gtk-3.0/gtk/deprecated/gtktable.h:126:1: note: 'gtk_table_attach' has been explicitly marked deprecated here
53:58.59   126 | GDK_DEPRECATED_IN_3_4_FOR(GtkGrid)
53:58.59       | ^
53:58.59 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:287:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_4_FOR'
53:58.59   287 | # define GDK_DEPRECATED_IN_3_4_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.59       |                                               ^
53:58.59 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.59    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.59       |                               ^
53:58.59 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.59  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.59       |                                            ^
53:58.59 In file included from Unified_cpp_widget_gtk2.cpp:119:
53:58.59 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/gtk/nsPrintDialogGTK.cpp:304:48: warning: 'gtk_vbox_new' is deprecated: Use 'gtk_box_new' instead [-Wdeprecated-declarations]
53:58.59   304 |   GtkWidget* header_footer_vertical_squasher = gtk_vbox_new(FALSE, 0);
53:58.59       |                                                ^
53:58.59 /usr/include/gtk-3.0/gtk/deprecated/gtkvbox.h:60:1: note: 'gtk_vbox_new' has been explicitly marked deprecated here
53:58.59    60 | GDK_DEPRECATED_IN_3_2_FOR(gtk_box_new)
53:58.59       | ^
53:58.59 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:273:47: note: expanded from macro 'GDK_DEPRECATED_IN_3_2_FOR'
53:58.59   273 | # define GDK_DEPRECATED_IN_3_2_FOR(f)         GDK_DEPRECATED_FOR(f)
53:58.59       |                                               ^
53:58.59 /usr/include/gtk-3.0/gdk/gdkversionmacros.h:49:31: note: expanded from macro 'GDK_DEPRECATED_FOR'
53:58.59    49 | #define GDK_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _GDK_EXTERN
53:58.59       |                               ^
53:58.59 /usr/include/glib-2.0/glib/gmacros.h:1273:44: note: expanded from macro 'G_DEPRECATED_FOR'
53:58.59  1273 | #define G_DEPRECATED_FOR(f) __attribute__((__deprecated__("Use '" #f "' instead")))
53:58.59       |                                            ^
54:06.37 29 warnings generated.
54:06.44 xpcom/build/Services.cpp.stub
54:36.84 In file included from Unified_cpp_xpcom_base2.cpp:65:
54:36.84 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/base/nsMemoryReporterManager.cpp:137:26: warning: 'mallinfo' is deprecated [-Wdeprecated-declarations]
54:36.84   137 |   struct mallinfo info = mallinfo();
54:36.84       |                          ^
54:36.84 /usr/include/malloc.h:114:48: note: 'mallinfo' has been explicitly marked deprecated here
54:36.84   114 | extern struct mallinfo mallinfo (void) __THROW __MALLOC_DEPRECATED;
54:36.84       |                                                ^
54:36.84 /usr/include/malloc.h:32:30: note: expanded from macro '__MALLOC_DEPRECATED'
54:36.84    32 | # define __MALLOC_DEPRECATED __attribute_deprecated__
54:36.84       |                              ^
54:36.84 /usr/include/aarch64-linux-gnu/sys/cdefs.h:356:51: note: expanded from macro '__attribute_deprecated__'
54:36.84   356 | # define __attribute_deprecated__ __attribute__ ((__deprecated__))
54:36.84       |                                                   ^
54:37.54 xpcom/components
54:43.39 1 warning generated.
54:46.94 xpcom/ds
54:49.12 xpcom/io
54:51.17 xpcom/reflect/xptcall/md/unix/xptcinvoke_asm_aarch64.o
54:51.17 xpcom/reflect/xptcall/md/unix/xptcstubs_asm_aarch64.o
54:51.25 xpcom/reflect/xptcall/md/unix
54:55.56 xpcom/reflect/xptcall
54:57.21 xpcom/reflect/xptinfo
54:58.66 xpcom/string
55:01.13 xpcom/threads
55:03.50 xpfe/appshell
55:07.63 js/xpconnect/shell
55:09.79 media/ffvpx/libavcodec/libmozavcodec.so.symbols.stub
55:12.77 media/ffvpx/libavcodec/aarch64
55:12.84 media/ffvpx/libavcodec/aarch64/idctdsp_neon.o
55:12.88 media/ffvpx/libavcodec/aarch64/mpegaudiodsp_neon.o
55:12.92 media/ffvpx/libavcodec/aarch64/simple_idct_neon.o
55:13.02 media/ffvpx/libavcodec/bsf
55:13.09 media/ffvpx/libavcodec
55:18.31 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/options.c:39:
55:18.31 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/options_table.h:50:110: warning: implicit conversion from 'long' to 'double' changes value from 9223372036854775807 to 9223372036854775808 [-Wimplicit-const-int-float-conversion]
55:18.31    50 | {"b", "set bitrate (in bits/s)", OFFSET(bit_rate), AV_OPT_TYPE_INT64, {.i64 = AV_CODEC_DEFAULT_BITRATE }, 0, INT64_MAX, A|V|E},
55:18.31       | ~                                                                                                            ^~~~~~~~~
55:18.31 /usr/include/stdint.h:113:22: note: expanded from macro 'INT64_MAX'
55:18.31   113 | # define INT64_MAX              (__INT64_C(9223372036854775807))
55:18.31       |                                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
55:18.31 /usr/include/stdint.h:95:24: note: expanded from macro '__INT64_C'
55:18.31    95 | #  define __INT64_C(c)  c ## L
55:18.31       |                         ^~~~~~
55:18.31 <scratch space>:184:1: note: expanded from here
55:18.31   184 | 9223372036854775807L
55:18.31       | ^~~~~~~~~~~~~~~~~~~~
55:18.34 1 warning generated.
55:18.68 media/ffvpx/libavutil/libmozavutil.so.symbols.stub
55:18.87 media/ffvpx/libavutil/aarch64
55:18.94 media/ffvpx/libavutil/aarch64/float_dsp_neon.o
55:19.01 media/ffvpx/libavutil/aarch64/tx_float_neon.o
55:19.20 media/ffvpx/libavutil
55:20.43 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/cpu.c:72:12: warning: 'return' will never be executed [-Wunreachable-code-return]
55:20.43    72 |     return 0;
55:20.43       |            ^
55:20.43 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/cpu.c:116:76: warning: implicit conversion from 'long' to 'double' changes value from 9223372036854775807 to 9223372036854775808 [-Wimplicit-const-int-float-conversion]
55:20.43   116 |         { "flags"   , NULL, 0, AV_OPT_TYPE_FLAGS, { .i64 = 0 }, INT64_MIN, INT64_MAX, .unit = "flags" },
55:20.43       |         ~                                                                  ^~~~~~~~~
55:20.43 /usr/include/stdint.h:113:22: note: expanded from macro 'INT64_MAX'
55:20.43   113 | # define INT64_MAX              (__INT64_C(9223372036854775807))
55:20.43       |                                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
55:20.43 /usr/include/stdint.h:95:24: note: expanded from macro '__INT64_C'
55:20.43    95 | #  define __INT64_C(c)  c ## L
55:20.43       |                         ^~~~~~
55:20.43 <scratch space>:20:1: note: expanded from here
55:20.43    20 | 9223372036854775807L
55:20.43       | ^~~~~~~~~~~~~~~~~~~~
55:20.43 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/cpu.c:284:12: warning: 'return' will never be executed [-Wunreachable-code-return]
55:20.43   284 |     return 8;
55:20.43       |            ^
55:20.44 3 warnings generated.
55:20.45 dom/media/eme/clearkey
55:20.72 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/eval.c:249:29: warning: implicit conversion from 'unsigned long' to 'double' changes value from 18446744073709551615 to 18446744073709551616 [-Wimplicit-const-int-float-conversion]
55:20.72   249 |             return r * (1.0/UINT64_MAX);
55:20.72       |                            ~^~~~~~~~~~
55:20.72 /usr/include/stdint.h:119:23: note: expanded from macro 'UINT64_MAX'
55:20.73   119 | # define UINT64_MAX             (__UINT64_C(18446744073709551615))
55:20.73       |                                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
55:20.73 /usr/include/stdint.h:96:25: note: expanded from macro '__UINT64_C'
55:20.73    96 | #  define __UINT64_C(c) c ## UL
55:20.73       |                         ^~~~~~~
55:20.73 <scratch space>:180:1: note: expanded from here
55:20.73   180 | 18446744073709551615UL
55:20.73       | ^~~~~~~~~~~~~~~~~~~~~~
55:20.73 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/eval.c:255:44: warning: implicit conversion from 'unsigned long' to 'double' changes value from 18446744073709551615 to 18446744073709551616 [-Wimplicit-const-int-float-conversion]
55:20.73   255 |             return min + (max - min) * r / UINT64_MAX;
55:20.73       |                                          ~ ^~~~~~~~~~
55:20.73 /usr/include/stdint.h:119:23: note: expanded from macro 'UINT64_MAX'
55:20.73   119 | # define UINT64_MAX             (__UINT64_C(18446744073709551615))
55:20.73       |                                  ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
55:20.73 /usr/include/stdint.h:96:25: note: expanded from macro '__UINT64_C'
55:20.73    96 | #  define __UINT64_C(c) c ## UL
55:20.73       |                         ^~~~~~~
55:20.73 <scratch space>:181:1: note: expanded from here
55:20.73   181 | 18446744073709551615UL
55:20.73       | ^~~~~~~~~~~~~~~~~~~~~~
55:20.88 2 warnings generated.
55:21.49 media/gmp-clearkey/0.1
55:22.33 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/opt.c:455:12: warning: 'return' will never be executed [-Wunreachable-code-return]
55:22.33   455 |     return 0;
55:22.33       |            ^
55:22.65 modules/xz-embedded
55:22.76 1 warning generated.
55:23.02 security/manager/ssl/builtins/dynamic-library/libnssckbi.so.symbols.stub
55:23.14 security/manager/ssl/ipcclientcerts/dynamic-library/libipcclientcerts.so.symbols.stub
55:23.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/time.c:68:12: warning: 'return' will never be executed [-Wunreachable-code-return]
55:23.29    68 |     return av_gettime() + 42 * 60 * 60 * INT64_C(1000000);
55:23.29       |            ^~~~~~~~~~
55:23.30 1 warning generated.
55:23.31 security/nss/cmd/certutil
55:23.82 security/nss/cmd/lib
55:24.54 security/nss/cmd/pk12util
55:25.28 security/nss/lib/ckfw
55:25.36 security/nss/lib/crmf
55:25.88 security/nss/lib/freebl/out.freebl_hash.def.stub
55:26.24 security/nss/lib/freebl/out.freebl_hash_vector.def.stub
55:26.65 security/nss/lib/jar
55:27.03 security/nss/lib/softoken/out.softokn.def.stub
55:27.15 security/nss/lib/softoken
55:27.52 toolkit/components/telemetry/pingsender
55:27.53 toolkit/xre/glxtest
55:28.14 widget/gtk/v4l2test
55:28.23 widget/gtk/vaapitest
55:28.70 build/pure_virtual/libpure_virtual.a
55:28.73 dom/media/fake-cdm/libfake.so
55:28.97 dom/media/gmp-plugin-openh264/libfakeopenh264.so
55:29.27 config/external/nspr/pr/libnspr4.so
55:29.43 config/external/gkcodecs/libgkcodecs.so
55:29.60 config/external/lgpllibs/liblgpllibs.so
55:29.79 config/external/sqlite/libmozsqlite3.so
55:29.83 dom/base
55:30.84 warning: trait `HasFloat` is never used
55:30.84   --> third_party/rust/bindgen/ir/item.rs:89:18
55:30.84    |
55:30.84 89 | pub(crate) trait HasFloat {
55:30.84    |                  ^^^^^^^^
55:30.84    |
55:30.84    = note: `#[warn(dead_code)]` (part of `#[warn(unused)]`) on by default
55:30.85 warning: hiding a lifetime that's elided elsewhere is confusing
55:30.85    --> third_party/rust/bindgen/lib.rs:968:21
55:30.85     |
55:30.85 968 |     fn rustfmt_path(&self) -> io::Result<Cow<PathBuf>> {
55:30.85     |                     ^^^^^                ^^^^^^^^^^^^ the same lifetime is hidden here
55:30.85     |                     |
55:30.85     |                     the lifetime is elided here
55:30.85     |
55:30.85     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:30.85     = note: `#[warn(mismatched_lifetime_syntaxes)]` on by default
55:30.85 help: use `'_` for type paths
55:30.85     |
55:30.85 968 |     fn rustfmt_path(&self) -> io::Result<Cow<'_, PathBuf>> {
55:30.85     |                                              +++
55:30.85 warning: hiding a lifetime that's elided elsewhere is confusing
55:30.85    --> third_party/rust/bindgen/clang.rs:946:26
55:30.85     |
55:30.85 946 |     pub(crate) fn tokens(&self) -> RawTokens {
55:30.85     |                          ^^^^^     ^^^^^^^^^ the same lifetime is hidden here
55:30.85     |                          |
55:30.85     |                          the lifetime is elided here
55:30.85     |
55:30.85     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:30.85 help: use `'_` for type paths
55:30.85     |
55:30.85 946 |     pub(crate) fn tokens(&self) -> RawTokens<'_> {
55:30.85     |                                             ++++
55:30.85 warning: hiding a lifetime that's elided elsewhere is confusing
55:30.85     --> third_party/rust/bindgen/clang.rs:1004:24
55:30.85      |
55:30.85 1004 |     pub(crate) fn iter(&self) -> ClangTokenIterator {
55:30.85      |                        ^^^^^     ^^^^^^^^^^^^^^^^^^ the same lifetime is hidden here
55:30.85      |                        |
55:30.85      |                        the lifetime is elided here
55:30.85      |
55:30.85      = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:30.85 help: use `'_` for type paths
55:30.85      |
55:30.85 1004 |     pub(crate) fn iter(&self) -> ClangTokenIterator<'_> {
55:30.85      |                                                    ++++
55:30.85 warning: hiding a lifetime that's elided elsewhere is confusing
55:30.85     --> third_party/rust/bindgen/ir/context.rs:1243:9
55:30.85      |
55:30.85 1243 |         &self,
55:30.85      |         ^^^^^ the lifetime is elided here
55:30.85 1244 |     ) -> traversal::AssertNoDanglingItemsTraversal {
55:30.85      |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ the same lifetime is hidden here
55:30.85      |
55:30.85      = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:30.85 help: use `'_` for type paths
55:30.85      |
55:30.85 1244 |     ) -> traversal::AssertNoDanglingItemsTraversal<'_> {
55:30.85      |                                                   ++++
55:30.85 warning: hiding a lifetime that's elided elsewhere is confusing
55:30.85    --> third_party/rust/bindgen/ir/ty.rs:246:28
55:30.85     |
55:30.85 246 |     fn sanitize_name(name: &str) -> Cow<str> {
55:30.85     |                            ^^^^     ^^^^^^^^ the same lifetime is hidden here
55:30.85     |                            |
55:30.85     |                            the lifetime is elided here
55:30.85     |
55:30.85     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:30.85 help: use `'_` for type paths
55:30.85     |
55:30.85 246 |     fn sanitize_name(name: &str) -> Cow<'_, str> {
55:30.85     |                                         +++
55:30.85 warning: `bindgen` (lib) generated 6 warnings (run `cargo fix --lib -p bindgen` to apply 5 suggestions)
55:30.85    Compiling builtins-static v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/builtins)
55:31.07 warning: unexpected `cfg` condition value: `testlib`
55:31.07    --> security/manager/ssl/builtins/build.rs:351:11
55:31.07     |
55:31.07 351 |     #[cfg(feature = "testlib")]
55:31.07     |           ^^^^^^^^^^^^^^^^^^^
55:31.07     |
55:31.07     = note: expected values for `feature` are: `mozilla-central-workspace-hack`
55:31.07     = help: consider adding `testlib` as a feature in `Cargo.toml`
55:31.07     = note: see <https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html> for more information about checking conditional configuration
55:31.07     = note: `#[warn(unexpected_cfgs)]` on by default
55:31.07 warning: unexpected `cfg` condition value: `testlib`
55:31.07    --> security/manager/ssl/builtins/build.rs:356:15
55:31.07     |
55:31.07 356 |     #[cfg(not(feature = "testlib"))]
55:31.07     |               ^^^^^^^^^^^^^^^^^^^
55:31.07     |
55:31.07     = note: expected values for `feature` are: `mozilla-central-workspace-hack`
55:31.07     = help: consider adding `testlib` as a feature in `Cargo.toml`
55:31.07     = note: see <https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html> for more information about checking conditional configuration
55:31.31 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.31    --> security/manager/ssl/builtins/build.rs:101:13
55:31.31     |
55:31.31 101 | fn class(i: &str) -> IResult<&str, Ck> {
55:31.31     |             ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.31     |             |                |
55:31.31     |             |                the same lifetime is elided here
55:31.31     |             the lifetime is elided here
55:31.31     |
55:31.31     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.31     = note: `#[warn(mismatched_lifetime_syntaxes)]` on by default
55:31.31 help: use `'_` for type paths
55:31.31     |
55:31.31 101 | fn class(i: &str) -> IResult<&str, Ck<'_>> {
55:31.31     |                                      ++++
55:31.31 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.31    --> security/manager/ssl/builtins/build.rs:114:13
55:31.31     |
55:31.31 114 | fn trust(i: &str) -> IResult<&str, Ck> {
55:31.31     |             ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.31     |             |                |
55:31.31     |             |                the same lifetime is elided here
55:31.31     |             the lifetime is elided here
55:31.31     |
55:31.31     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.31 help: use `'_` for type paths
55:31.31     |
55:31.31 114 | fn trust(i: &str) -> IResult<&str, Ck<'_>> {
55:31.31     |                                      ++++
55:31.31 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.31    --> security/manager/ssl/builtins/build.rs:129:20
55:31.31     |
55:31.31 129 | fn option_bbool(i: &str) -> IResult<&str, Ck> {
55:31.31     |                    ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.31     |                    |                |
55:31.31     |                    |                the same lifetime is elided here
55:31.31     |                    the lifetime is elided here
55:31.31     |
55:31.31     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 129 | fn option_bbool(i: &str) -> IResult<&str, Ck<'_>> {
55:31.32     |                                             ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:138:18
55:31.32     |
55:31.32 138 | fn bbool_true(i: &str) -> IResult<&str, Ck> {
55:31.32     |                  ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.32     |                  |                |
55:31.32     |                  |                the same lifetime is elided here
55:31.32     |                  the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 138 | fn bbool_true(i: &str) -> IResult<&str, Ck<'_>> {
55:31.32     |                                           ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:147:19
55:31.32     |
55:31.32 147 | fn bbool_false(i: &str) -> IResult<&str, Ck> {
55:31.32     |                   ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.32     |                   |                |
55:31.32     |                   |                the same lifetime is elided here
55:31.32     |                   the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 147 | fn bbool_false(i: &str) -> IResult<&str, Ck<'_>> {
55:31.32     |                                            ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:156:12
55:31.32     |
55:31.32 156 | fn utf8(i: &str) -> IResult<&str, Ck> {
55:31.32     |            ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.32     |            |                |
55:31.32     |            |                the same lifetime is elided here
55:31.32     |            the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 156 | fn utf8(i: &str) -> IResult<&str, Ck<'_>> {
55:31.32     |                                     ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:167:24
55:31.32     |
55:31.32 167 | fn certificate_type(i: &str) -> IResult<&str, Ck> {
55:31.32     |                        ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.32     |                        |                |
55:31.32     |                        |                the same lifetime is elided here
55:31.32     |                        the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 167 | fn certificate_type(i: &str) -> IResult<&str, Ck<'_>> {
55:31.32     |                                                 ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:178:22
55:31.32     |
55:31.32 178 | fn distrust_after(i: &str) -> IResult<&str, Ck> {
55:31.32     |                      ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.32     |                      |                |
55:31.32     |                      |                the same lifetime is elided here
55:31.32     |                      the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 178 | fn distrust_after(i: &str) -> IResult<&str, Ck<'_>> {
55:31.32     |                                               ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:196:23
55:31.32     |
55:31.32 196 | fn multiline_octal(i: &str) -> IResult<&str, Ck> {
55:31.32     |                       ^^^^             ^^^^  ^^ the same lifetime is hidden here
55:31.32     |                       |                |
55:31.32     |                       |                the same lifetime is elided here
55:31.32     |                       the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 196 | fn multiline_octal(i: &str) -> IResult<&str, Ck<'_>> {
55:31.32     |                                                ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:207:24
55:31.32     |
55:31.32 207 | fn distrust_comment(i: &str) -> IResult<&str, (&str, Ck)> {
55:31.32     |                        ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
55:31.32     |                        |                |      |
55:31.32     |                        |                |      the same lifetime is elided here
55:31.32     |                        |                the same lifetime is elided here
55:31.32     |                        the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 207 | fn distrust_comment(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
55:31.32     |                                                        ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:219:15
55:31.32     |
55:31.32 219 | fn comment(i: &str) -> IResult<&str, (&str, Ck)> {
55:31.32     |               ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
55:31.32     |               |                |      |
55:31.32     |               |                |      the same lifetime is elided here
55:31.32     |               |                the same lifetime is elided here
55:31.32     |               the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 219 | fn comment(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
55:31.32     |                                               ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:224:21
55:31.32     |
55:31.32 224 | fn certdata_line(i: &str) -> IResult<&str, (&str, Ck)> {
55:31.32     |                     ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
55:31.32     |                     |                |      |
55:31.32     |                     |                |      the same lifetime is elided here
55:31.32     |                     |                the same lifetime is elided here
55:31.32     |                     the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 224 | fn certdata_line(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
55:31.32     |                                                     ++++
55:31.32 warning: hiding a lifetime that's elided elsewhere is confusing
55:31.32    --> security/manager/ssl/builtins/build.rs:281:13
55:31.32     |
55:31.32 281 | fn parse(i: &str) -> IResult<&str, Vec<Block>> {
55:31.32     |             ^^^^             ^^^^      ^^^^^ the same lifetime is hidden here
55:31.32     |             |                |
55:31.32     |             |                the same lifetime is elided here
55:31.32     |             the lifetime is elided here
55:31.32     |
55:31.32     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
55:31.32 help: use `'_` for type paths
55:31.32     |
55:31.32 281 | fn parse(i: &str) -> IResult<&str, Vec<Block<'_>>> {
55:31.32     |                                             ++++
55:32.94 warning: `builtins-static` (build script) generated 15 warnings
55:32.94    Compiling mozilla-central-workspace-hack v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/build/workspace-hack)
55:37.01     Finished `release` profile [optimized] target(s) in 8.36s
55:37.87 security/manager/ssl/builtins/libbuiltins_static.a
55:40.90 dom/origin-trials
56:07.34 js/src/gc
56:09.52 layout/style
56:15.75 media/libdav1d
56:16.23 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/third_party/dav1d/src/cpu.c:110:9: warning: code will never be executed [-Wunreachable-code]
56:16.23   110 |     if (c)
56:16.23       |         ^
56:16.24 1 warning generated.
56:33.82 netwerk/base
57:12.54 netwerk/dns
57:35.92 security/manager/ssl
58:11.29 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
58:11.29 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
58:11.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:91:11: error: redefinition of 'end' with a different type: 'char *' vs 'size_t' (aka 'unsigned long')
58:11.29    91 |     char* end = nullptr;
58:11.29       |           ^
58:11.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:83:12: note: previous definition is here
58:11.29    83 |     size_t end = token.find_last_not_of(" \t");
58:11.29       |            ^
58:11.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:92:53: error: cannot initialize a parameter of type 'char **' with an rvalue of type 'size_t *' (aka 'unsigned long *')
58:11.29    92 |     unsigned long val = std::strtoul(token.c_str(), &end, 16);
58:11.29       |                                                     ^~~~
58:11.29 /usr/include/stdlib.h:221:26: note: passing argument to parameter '__endptr' here
58:11.29   221 |                                           char **__restrict __endptr,
58:11.29       |                                                             ^
58:11.29 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
58:11.29 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
58:11.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:27: error: comparison between pointer and integer ('size_t' (aka 'unsigned long') and 'const char *')
58:11.29    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
58:11.29       |                       ~~~ ^  ~~~~~~~~~~~~~
58:11.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:47: error: indirection requires pointer operand ('size_t' (aka 'unsigned long') invalid)
58:11.29    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
58:11.29       |                                               ^~~~
58:18.66 4 errors generated.
58:18.72 gmake[5]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:676: Unified_cpp_security_manager_ssl2.o] Error 1
58:18.72 gmake[5]: *** Waiting for unfinished jobs....
58:20.30 gmake[4]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:72: security/manager/ssl/target-objects] Error 2
58:20.30 gmake[4]: *** Waiting for unfinished jobs....
59:15.68 gmake[3]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:34: compile] Error 2
59:15.86 gmake[2]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:359: default] Error 2
59:15.91 gmake[1]: *** [client.mk:60: build] Error 2
59:16.02 W 242 compiler warnings present.
59:17.01 W Notification center failed: Install notify-send (usually part of the libnotify package) to get a notification when the build finishes.
 Config object not found by mach.
Configure complete!
Be sure to run |mach build| to pick up any changes
  Parallelism determined by memory: using 4 jobs for 4 cores based on 15.6 GiB RAM and estimated job size of 1.0 GiB
make: *** [Makefile:132: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.
build(Linux, i686, ubuntu.24.04)

……
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/parsers.c:21:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/avcodec.h:32:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avutil.h:301:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.09 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.09   319 | #define HAVE_MEMALIGN 0
98:54.09       |         ^
98:54.09 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:54.09    70 | #define HAVE_MEMALIGN 1
98:54.09       |         ^
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/parsers.c:21:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/avcodec.h:32:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avutil.h:301:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
98:54.09 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.09 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.09   325 | #define HAVE_POSIX_MEMALIGN 0
98:54.09       |         ^
98:54.09 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:54.09    76 | #define HAVE_POSIX_MEMALIGN 1
98:54.09       |         ^
98:54.12 3 warnings generated.
98:54.16 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pcm.c:27:
98:54.16 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.16 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:54.16   234 | #define HAVE_MALLOC_H 0
98:54.16       |         ^
98:54.16 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:54.17    68 | #define HAVE_MALLOC_H 1
98:54.17       |         ^
98:54.17 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pcm.c:27:
98:54.17 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.17 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.17   319 | #define HAVE_MEMALIGN 0
98:54.17       |         ^
98:54.17 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:54.17    70 | #define HAVE_MEMALIGN 1
98:54.17       |         ^
98:54.17 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pcm.c:27:
98:54.17 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.17 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.17   325 | #define HAVE_POSIX_MEMALIGN 0
98:54.17       |         ^
98:54.17 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:54.17    76 | #define HAVE_POSIX_MEMALIGN 1
98:54.17       |         ^
98:54.50 3 warnings generated.
98:54.54 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/profiles.c:19:
98:54.54 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:54.55   234 | #define HAVE_MALLOC_H 0
98:54.55       |         ^
98:54.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:54.55    68 | #define HAVE_MALLOC_H 1
98:54.55       |         ^
98:54.55 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/profiles.c:19:
98:54.55 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.55   319 | #define HAVE_MEMALIGN 0
98:54.55       |         ^
98:54.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:54.55    70 | #define HAVE_MEMALIGN 1
98:54.55       |         ^
98:54.55 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/profiles.c:19:
98:54.55 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.55   325 | #define HAVE_POSIX_MEMALIGN 0
98:54.55       |         ^
98:54.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:54.55    76 | #define HAVE_POSIX_MEMALIGN 1
98:54.55       |         ^
98:54.62 3 warnings generated.
98:54.66 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread.c:32:
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/thread.h:25:
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:54.67   234 | #define HAVE_MALLOC_H 0
98:54.67       |         ^
98:54.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:54.67    68 | #define HAVE_MALLOC_H 1
98:54.67       |         ^
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread.c:32:
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/thread.h:25:
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.67   319 | #define HAVE_MEMALIGN 0
98:54.67       |         ^
98:54.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:54.67    70 | #define HAVE_MEMALIGN 1
98:54.67       |         ^
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread.c:32:
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/thread.h:25:
98:54.67 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.67   325 | #define HAVE_POSIX_MEMALIGN 0
98:54.67       |         ^
98:54.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:54.67    76 | #define HAVE_POSIX_MEMALIGN 1
98:54.67       |         ^
98:54.79 3 warnings generated.
98:54.84 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread_frame.c:25:
98:54.84 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.84 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:54.84   234 | #define HAVE_MALLOC_H 0
98:54.84       |         ^
98:54.84 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:54.84    68 | #define HAVE_MALLOC_H 1
98:54.84       |         ^
98:54.84 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread_frame.c:25:
98:54.84 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.84 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.84   319 | #define HAVE_MEMALIGN 0
98:54.84       |         ^
98:54.84 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:54.84    70 | #define HAVE_MEMALIGN 1
98:54.84       |         ^
98:54.84 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread_frame.c:25:
98:54.84 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:54.84 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:54.84   325 | #define HAVE_POSIX_MEMALIGN 0
98:54.84       |         ^
98:54.84 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:54.84    76 | #define HAVE_POSIX_MEMALIGN 1
98:54.84       |         ^
98:55.02 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread_slice.c:25:
98:55.02 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.02 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:55.02   234 | #define HAVE_MALLOC_H 0
98:55.02       |         ^
98:55.02 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:55.02    68 | #define HAVE_MALLOC_H 1
98:55.02       |         ^
98:55.02 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread_slice.c:25:
98:55.02 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.02 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:55.02   319 | #define HAVE_MEMALIGN 0
98:55.02       |         ^
98:55.02 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:55.02    70 | #define HAVE_MEMALIGN 1
98:55.02       |         ^
98:55.02 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pthread_slice.c:25:
98:55.02 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.02 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:55.02   325 | #define HAVE_POSIX_MEMALIGN 0
98:55.02       |         ^
98:55.02 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:55.03    76 | #define HAVE_POSIX_MEMALIGN 1
98:55.03       |         ^
98:55.15 3 warnings generated.
98:55.17 media/gmp-clearkey/0.1
98:55.18 3 warnings generated.
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/refstruct.c:25:
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avassert.h:32:
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.26 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:55.26   234 | #define HAVE_MALLOC_H 0
98:55.26       |         ^
98:55.26 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:55.26    68 | #define HAVE_MALLOC_H 1
98:55.26       |         ^
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/refstruct.c:25:
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avassert.h:32:
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.26 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:55.26   319 | #define HAVE_MEMALIGN 0
98:55.26       |         ^
98:55.26 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:55.26    70 | #define HAVE_MEMALIGN 1
98:55.26       |         ^
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/refstruct.c:25:
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avassert.h:32:
98:55.26 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.26 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:55.26   325 | #define HAVE_POSIX_MEMALIGN 0
98:55.26       |         ^
98:55.26 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:55.26    76 | #define HAVE_POSIX_MEMALIGN 1
98:55.26       |         ^
98:55.36 3 warnings generated.
98:55.45 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/simple_idct.c:28:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/intreadwrite.h:25:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/bswap.h:35:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:55.46   234 | #define HAVE_MALLOC_H 0
98:55.46       |         ^
98:55.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:55.46    68 | #define HAVE_MALLOC_H 1
98:55.46       |         ^
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/simple_idct.c:28:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/intreadwrite.h:25:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/bswap.h:35:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:55.46   319 | #define HAVE_MEMALIGN 0
98:55.46       |         ^
98:55.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:55.46    70 | #define HAVE_MEMALIGN 1
98:55.46       |         ^
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/simple_idct.c:28:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/intreadwrite.h:25:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/bswap.h:35:
98:55.46 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:55.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:55.46   325 | #define HAVE_POSIX_MEMALIGN 0
98:55.46       |         ^
98:55.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:55.46    76 | #define HAVE_POSIX_MEMALIGN 1
98:55.46       |         ^
98:56.25 3 warnings generated.
98:56.29 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/utils.c:28:
98:56.29 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:56.29   234 | #define HAVE_MALLOC_H 0
98:56.30       |         ^
98:56.30 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:56.30    68 | #define HAVE_MALLOC_H 1
98:56.30       |         ^
98:56.30 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/utils.c:28:
98:56.30 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.30 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:56.30   319 | #define HAVE_MEMALIGN 0
98:56.30       |         ^
98:56.30 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:56.30    70 | #define HAVE_MEMALIGN 1
98:56.30       |         ^
98:56.30 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/utils.c:28:
98:56.30 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.30 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:56.30   325 | #define HAVE_POSIX_MEMALIGN 0
98:56.30       |         ^
98:56.30 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:56.30    76 | #define HAVE_POSIX_MEMALIGN 1
98:56.30       |         ^
98:56.68 3 warnings generated.
98:56.72 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/version.c:23:
98:56.72 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.72 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:56.72   234 | #define HAVE_MALLOC_H 0
98:56.72       |         ^
98:56.72 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:56.72    68 | #define HAVE_MALLOC_H 1
98:56.72       |         ^
98:56.72 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/version.c:23:
98:56.72 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.72 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:56.72   319 | #define HAVE_MEMALIGN 0
98:56.72       |         ^
98:56.72 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:56.72    70 | #define HAVE_MEMALIGN 1
98:56.72       |         ^
98:56.72 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/version.c:23:
98:56.72 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.73 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:56.73   325 | #define HAVE_POSIX_MEMALIGN 0
98:56.73       |         ^
98:56.73 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:56.73    76 | #define HAVE_POSIX_MEMALIGN 1
98:56.73       |         ^
98:56.81 3 warnings generated.
98:56.87 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vlc.c:30:
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avassert.h:32:
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.88 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:56.88   234 | #define HAVE_MALLOC_H 0
98:56.88       |         ^
98:56.88 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:56.88    68 | #define HAVE_MALLOC_H 1
98:56.88       |         ^
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vlc.c:30:
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avassert.h:32:
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.88 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:56.88   319 | #define HAVE_MEMALIGN 0
98:56.88       |         ^
98:56.88 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:56.88    70 | #define HAVE_MEMALIGN 1
98:56.88       |         ^
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vlc.c:30:
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avassert.h:32:
98:56.88 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:56.88 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:56.88   325 | #define HAVE_POSIX_MEMALIGN 0
98:56.88       |         ^
98:56.88 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:56.88    76 | #define HAVE_POSIX_MEMALIGN 1
98:56.88       |         ^
98:57.21 3 warnings generated.
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vorbis_data.c:22:
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/mem_internal.h:24:
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:57.27   234 | #define HAVE_MALLOC_H 0
98:57.27       |         ^
98:57.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:57.27    68 | #define HAVE_MALLOC_H 1
98:57.27       |         ^
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vorbis_data.c:22:
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/mem_internal.h:24:
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:57.27   319 | #define HAVE_MEMALIGN 0
98:57.27       |         ^
98:57.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:57.27    70 | #define HAVE_MEMALIGN 1
98:57.27       |         ^
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vorbis_data.c:22:
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/mem_internal.h:24:
98:57.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:57.27   325 | #define HAVE_POSIX_MEMALIGN 0
98:57.27       |         ^
98:57.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:57.27    76 | #define HAVE_POSIX_MEMALIGN 1
98:57.27       |         ^
98:57.31 3 warnings generated.
98:57.33 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vorbis_parser.c:33:
98:57.33 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/get_bits.h:31:
98:57.33 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
98:57.33 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:57.34   234 | #define HAVE_MALLOC_H 0
98:57.34       |         ^
98:57.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:57.34    68 | #define HAVE_MALLOC_H 1
98:57.34       |         ^
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vorbis_parser.c:33:
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/get_bits.h:31:
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:57.34   319 | #define HAVE_MEMALIGN 0
98:57.34       |         ^
98:57.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:57.34    70 | #define HAVE_MEMALIGN 1
98:57.34       |         ^
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vorbis_parser.c:33:
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/get_bits.h:31:
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
98:57.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:57.34   325 | #define HAVE_POSIX_MEMALIGN 0
98:57.34       |         ^
98:57.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:57.34    76 | #define HAVE_POSIX_MEMALIGN 1
98:57.34       |         ^
98:57.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/xiph.c:23:
98:57.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/intreadwrite.h:25:
98:57.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/bswap.h:35:
98:57.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.35 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:234:9: warning: 'HAVE_MALLOC_H' macro redefined [-Wmacro-redefined]
98:57.36   234 | #define HAVE_MALLOC_H 0
98:57.36       |         ^
98:57.36 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:68:9: note: previous definition is here
98:57.36    68 | #define HAVE_MALLOC_H 1
98:57.36       |         ^
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/xiph.c:23:
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/intreadwrite.h:25:
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/bswap.h:35:
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.36 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:319:9: warning: 'HAVE_MEMALIGN' macro redefined [-Wmacro-redefined]
98:57.36   319 | #define HAVE_MEMALIGN 0
98:57.36       |         ^
98:57.36 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:70:9: note: previous definition is here
98:57.36    70 | #define HAVE_MEMALIGN 1
98:57.36       |         ^
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/xiph.c:23:
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/intreadwrite.h:25:
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/bswap.h:35:
98:57.36 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:19:
98:57.36 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_generic.h:325:9: warning: 'HAVE_POSIX_MEMALIGN' macro redefined [-Wmacro-redefined]
98:57.36   325 | #define HAVE_POSIX_MEMALIGN 0
98:57.36       |         ^
98:57.36 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/mozilla-config.h:76:9: note: previous definition is here
98:57.36    76 | #define HAVE_POSIX_MEMALIGN 1
98:57.36       |         ^
98:57.38 3 warnings generated.
98:57.40 modules/xz-embedded
98:57.49 3 warnings generated.
98:57.50 security/manager/ssl/builtins/dynamic-library/libnssckbi.so.symbols.stub
98:57.75 security/manager/ssl/ipcclientcerts/dynamic-library/libipcclientcerts.so.symbols.stub
98:57.98 security/nss/cmd/certutil
98:59.16 security/nss/cmd/lib
98:59.16 security/nss/cmd/pk12util
98:59.57 security/nss/lib/ckfw
99:00.38 security/nss/lib/crmf
99:01.85 security/nss/lib/freebl/out.freebl_hash.def.stub
99:02.40 security/nss/lib/freebl/out.freebl_hash_vector.def.stub
99:02.88 security/nss/lib/jar
99:04.29 security/nss/lib/softoken/out.softokn.def.stub
99:04.55 security/nss/lib/softoken
99:05.26 toolkit/components/telemetry/pingsender
99:06.10 toolkit/xre/glxtest
99:07.26 tools/power
99:07.27 widget/gtk/vaapitest
99:08.65 build/pure_virtual/libpure_virtual.a
99:08.83 dom/media/fake-cdm/libfake.so
99:08.84 dom/media/gmp-plugin-openh264/libfakeopenh264.so
99:09.17 config/external/nspr/pr/libnspr4.so
99:09.18 config/external/lgpllibs/liblgpllibs.so
99:09.18 config/external/gkcodecs/libgkcodecs.so
99:09.48 config/external/sqlite/libmozsqlite3.so
99:09.51 dom/base
99:09.85 dom/origin-trials
99:12.32 warning: trait `HasFloat` is never used
99:12.33   --> third_party/rust/bindgen/ir/item.rs:89:18
99:12.33    |
99:12.33 89 | pub(crate) trait HasFloat {
99:12.33    |                  ^^^^^^^^
99:12.33    |
99:12.33    = note: `#[warn(dead_code)]` (part of `#[warn(unused)]`) on by default
99:12.33 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.33    --> third_party/rust/bindgen/lib.rs:968:21
99:12.33     |
99:12.33 968 |     fn rustfmt_path(&self) -> io::Result<Cow<PathBuf>> {
99:12.33     |                     ^^^^^                ^^^^^^^^^^^^ the same lifetime is hidden here
99:12.33     |                     |
99:12.33     |                     the lifetime is elided here
99:12.33     |
99:12.33     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.33     = note: `#[warn(mismatched_lifetime_syntaxes)]` on by default
99:12.33 help: use `'_` for type paths
99:12.33     |
99:12.33 968 |     fn rustfmt_path(&self) -> io::Result<Cow<'_, PathBuf>> {
99:12.33     |                                              +++
99:12.33 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.33    --> third_party/rust/bindgen/clang.rs:946:26
99:12.33     |
99:12.33 946 |     pub(crate) fn tokens(&self) -> RawTokens {
99:12.33     |                          ^^^^^     ^^^^^^^^^ the same lifetime is hidden here
99:12.33     |                          |
99:12.33     |                          the lifetime is elided here
99:12.33     |
99:12.33     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.33 help: use `'_` for type paths
99:12.33     |
99:12.33 946 |     pub(crate) fn tokens(&self) -> RawTokens<'_> {
99:12.33     |                                             ++++
99:12.33 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.33     --> third_party/rust/bindgen/clang.rs:1004:24
99:12.33      |
99:12.33 1004 |     pub(crate) fn iter(&self) -> ClangTokenIterator {
99:12.33      |                        ^^^^^     ^^^^^^^^^^^^^^^^^^ the same lifetime is hidden here
99:12.33      |                        |
99:12.33      |                        the lifetime is elided here
99:12.33      |
99:12.34      = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.34 help: use `'_` for type paths
99:12.34      |
99:12.34 1004 |     pub(crate) fn iter(&self) -> ClangTokenIterator<'_> {
99:12.34      |                                                    ++++
99:12.34 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.34     --> third_party/rust/bindgen/ir/context.rs:1243:9
99:12.34      |
99:12.34 1243 |         &self,
99:12.34      |         ^^^^^ the lifetime is elided here
99:12.34 1244 |     ) -> traversal::AssertNoDanglingItemsTraversal {
99:12.34      |          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ the same lifetime is hidden here
99:12.34      |
99:12.34      = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.34 help: use `'_` for type paths
99:12.34      |
99:12.34 1244 |     ) -> traversal::AssertNoDanglingItemsTraversal<'_> {
99:12.34      |                                                   ++++
99:12.34 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.34    --> third_party/rust/bindgen/ir/ty.rs:246:28
99:12.34     |
99:12.34 246 |     fn sanitize_name(name: &str) -> Cow<str> {
99:12.34     |                            ^^^^     ^^^^^^^^ the same lifetime is hidden here
99:12.34     |                            |
99:12.34     |                            the lifetime is elided here
99:12.34     |
99:12.34     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.34 help: use `'_` for type paths
99:12.34     |
99:12.34 246 |     fn sanitize_name(name: &str) -> Cow<'_, str> {
99:12.34     |                                         +++
99:12.34 warning: `bindgen` (lib) generated 6 warnings (run `cargo fix --lib -p bindgen` to apply 5 suggestions)
99:12.34    Compiling builtins-static v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/builtins)
99:12.69 warning: unexpected `cfg` condition value: `testlib`
99:12.69    --> security/manager/ssl/builtins/build.rs:351:11
99:12.69     |
99:12.69 351 |     #[cfg(feature = "testlib")]
99:12.69     |           ^^^^^^^^^^^^^^^^^^^
99:12.69     |
99:12.69     = note: expected values for `feature` are: `mozilla-central-workspace-hack`
99:12.69     = help: consider adding `testlib` as a feature in `Cargo.toml`
99:12.69     = note: see <https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html> for more information about checking conditional configuration
99:12.69     = note: `#[warn(unexpected_cfgs)]` on by default
99:12.69 warning: unexpected `cfg` condition value: `testlib`
99:12.69    --> security/manager/ssl/builtins/build.rs:356:15
99:12.69     |
99:12.69 356 |     #[cfg(not(feature = "testlib"))]
99:12.69     |               ^^^^^^^^^^^^^^^^^^^
99:12.69     |
99:12.69     = note: expected values for `feature` are: `mozilla-central-workspace-hack`
99:12.69     = help: consider adding `testlib` as a feature in `Cargo.toml`
99:12.69     = note: see <https://doc.rust-lang.org/nightly/rustc/check-cfg/cargo-specifics.html> for more information about checking conditional configuration
99:12.91 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.91    --> security/manager/ssl/builtins/build.rs:101:13
99:12.91     |
99:12.91 101 | fn class(i: &str) -> IResult<&str, Ck> {
99:12.91     |             ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.91     |             |                |
99:12.91     |             |                the same lifetime is elided here
99:12.91     |             the lifetime is elided here
99:12.91     |
99:12.91     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.91     = note: `#[warn(mismatched_lifetime_syntaxes)]` on by default
99:12.91 help: use `'_` for type paths
99:12.91     |
99:12.91 101 | fn class(i: &str) -> IResult<&str, Ck<'_>> {
99:12.91     |                                      ++++
99:12.91 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.91    --> security/manager/ssl/builtins/build.rs:114:13
99:12.91     |
99:12.91 114 | fn trust(i: &str) -> IResult<&str, Ck> {
99:12.91     |             ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.91     |             |                |
99:12.91     |             |                the same lifetime is elided here
99:12.91     |             the lifetime is elided here
99:12.91     |
99:12.91     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.91 help: use `'_` for type paths
99:12.91     |
99:12.91 114 | fn trust(i: &str) -> IResult<&str, Ck<'_>> {
99:12.91     |                                      ++++
99:12.91 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.91    --> security/manager/ssl/builtins/build.rs:129:20
99:12.91     |
99:12.92 129 | fn option_bbool(i: &str) -> IResult<&str, Ck> {
99:12.92     |                    ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.92     |                    |                |
99:12.92     |                    |                the same lifetime is elided here
99:12.92     |                    the lifetime is elided here
99:12.92     |
99:12.92     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.92 help: use `'_` for type paths
99:12.92     |
99:12.92 129 | fn option_bbool(i: &str) -> IResult<&str, Ck<'_>> {
99:12.92     |                                             ++++
99:12.92 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.92    --> security/manager/ssl/builtins/build.rs:138:18
99:12.92     |
99:12.92 138 | fn bbool_true(i: &str) -> IResult<&str, Ck> {
99:12.92     |                  ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.92     |                  |                |
99:12.92     |                  |                the same lifetime is elided here
99:12.92     |                  the lifetime is elided here
99:12.92     |
99:12.92     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.92 help: use `'_` for type paths
99:12.92     |
99:12.92 138 | fn bbool_true(i: &str) -> IResult<&str, Ck<'_>> {
99:12.92     |                                           ++++
99:12.92 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.92    --> security/manager/ssl/builtins/build.rs:147:19
99:12.92     |
99:12.92 147 | fn bbool_false(i: &str) -> IResult<&str, Ck> {
99:12.92     |                   ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.92     |                   |                |
99:12.92     |                   |                the same lifetime is elided here
99:12.92     |                   the lifetime is elided here
99:12.92     |
99:12.92     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.92 help: use `'_` for type paths
99:12.92     |
99:12.92 147 | fn bbool_false(i: &str) -> IResult<&str, Ck<'_>> {
99:12.92     |                                            ++++
99:12.92 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.92    --> security/manager/ssl/builtins/build.rs:156:12
99:12.92     |
99:12.92 156 | fn utf8(i: &str) -> IResult<&str, Ck> {
99:12.92     |            ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.92     |            |                |
99:12.92     |            |                the same lifetime is elided here
99:12.92     |            the lifetime is elided here
99:12.92     |
99:12.92     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.92 help: use `'_` for type paths
99:12.92     |
99:12.92 156 | fn utf8(i: &str) -> IResult<&str, Ck<'_>> {
99:12.92     |                                     ++++
99:12.92 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.92    --> security/manager/ssl/builtins/build.rs:167:24
99:12.92     |
99:12.92 167 | fn certificate_type(i: &str) -> IResult<&str, Ck> {
99:12.92     |                        ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.92     |                        |                |
99:12.92     |                        |                the same lifetime is elided here
99:12.92     |                        the lifetime is elided here
99:12.92     |
99:12.92     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.93 help: use `'_` for type paths
99:12.93     |
99:12.93 167 | fn certificate_type(i: &str) -> IResult<&str, Ck<'_>> {
99:12.93     |                                                 ++++
99:12.93 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.93    --> security/manager/ssl/builtins/build.rs:178:22
99:12.93     |
99:12.93 178 | fn distrust_after(i: &str) -> IResult<&str, Ck> {
99:12.93     |                      ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.93     |                      |                |
99:12.93     |                      |                the same lifetime is elided here
99:12.93     |                      the lifetime is elided here
99:12.93     |
99:12.93     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.93 help: use `'_` for type paths
99:12.93     |
99:12.93 178 | fn distrust_after(i: &str) -> IResult<&str, Ck<'_>> {
99:12.93     |                                               ++++
99:12.93 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.93    --> security/manager/ssl/builtins/build.rs:196:23
99:12.93     |
99:12.93 196 | fn multiline_octal(i: &str) -> IResult<&str, Ck> {
99:12.93     |                       ^^^^             ^^^^  ^^ the same lifetime is hidden here
99:12.93     |                       |                |
99:12.93     |                       |                the same lifetime is elided here
99:12.93     |                       the lifetime is elided here
99:12.93     |
99:12.93     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.93 help: use `'_` for type paths
99:12.93     |
99:12.93 196 | fn multiline_octal(i: &str) -> IResult<&str, Ck<'_>> {
99:12.93     |                                                ++++
99:12.93 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.93    --> security/manager/ssl/builtins/build.rs:207:24
99:12.93     |
99:12.93 207 | fn distrust_comment(i: &str) -> IResult<&str, (&str, Ck)> {
99:12.93     |                        ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
99:12.93     |                        |                |      |
99:12.93     |                        |                |      the same lifetime is elided here
99:12.93     |                        |                the same lifetime is elided here
99:12.93     |                        the lifetime is elided here
99:12.93     |
99:12.93     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.93 help: use `'_` for type paths
99:12.93     |
99:12.93 207 | fn distrust_comment(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
99:12.93     |                                                        ++++
99:12.93 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.93    --> security/manager/ssl/builtins/build.rs:219:15
99:12.93     |
99:12.93 219 | fn comment(i: &str) -> IResult<&str, (&str, Ck)> {
99:12.93     |               ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
99:12.93     |               |                |      |
99:12.93     |               |                |      the same lifetime is elided here
99:12.93     |               |                the same lifetime is elided here
99:12.93     |               the lifetime is elided here
99:12.93     |
99:12.93     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.93 help: use `'_` for type paths
99:12.93     |
99:12.93 219 | fn comment(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
99:12.93     |                                               ++++
99:12.93 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.93    --> security/manager/ssl/builtins/build.rs:224:21
99:12.93     |
99:12.93 224 | fn certdata_line(i: &str) -> IResult<&str, (&str, Ck)> {
99:12.93     |                     ^^^^             ^^^^   ^^^^  ^^ the same lifetime is hidden here
99:12.94     |                     |                |      |
99:12.94     |                     |                |      the same lifetime is elided here
99:12.94     |                     |                the same lifetime is elided here
99:12.94     |                     the lifetime is elided here
99:12.94     |
99:12.94     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.94 help: use `'_` for type paths
99:12.94     |
99:12.94 224 | fn certdata_line(i: &str) -> IResult<&str, (&str, Ck<'_>)> {
99:12.94     |                                                     ++++
99:12.94 warning: hiding a lifetime that's elided elsewhere is confusing
99:12.94    --> security/manager/ssl/builtins/build.rs:281:13
99:12.94     |
99:12.94 281 | fn parse(i: &str) -> IResult<&str, Vec<Block>> {
99:12.94     |             ^^^^             ^^^^      ^^^^^ the same lifetime is hidden here
99:12.94     |             |                |
99:12.94     |             |                the same lifetime is elided here
99:12.94     |             the lifetime is elided here
99:12.94     |
99:12.94     = help: the same lifetime is referred to in inconsistent ways, making the signature confusing
99:12.94 help: use `'_` for type paths
99:12.94     |
99:12.94 281 | fn parse(i: &str) -> IResult<&str, Vec<Block<'_>>> {
99:12.94     |                                             ++++
99:15.30 warning: `builtins-static` (build script) generated 15 warnings
99:15.30    Compiling mozilla-central-workspace-hack v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/build/workspace-hack)
99:21.37 In file included from Unified_cpp_dom_origin-trials0.cpp:2:
99:21.37 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/origin-trials/OriginTrials.cpp:23:
99:21.37 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/WebCryptoCommon.h:30:
99:21.37 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
99:21.37   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
99:21.38       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
99:22.28     Finished `release` profile [optimized] target(s) in 14.38s
99:22.80 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/nsContentUtils.cpp:28:
99:22.80 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
99:22.80   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
99:22.80       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
99:23.48 security/manager/ssl/builtins/libbuiltins_static.a
99:23.77 1 warning generated.
99:29.62 js/src/gc
99:51.82 layout/style
99:53.02 1 warning generated.
99:53.12 media/libdav1d
99:54.24 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/third_party/dav1d/src/cpu.c:110:9: warning: code will never be executed [-Wunreachable-code]
99:54.24   110 |     if (c)
99:54.24       |         ^
99:54.25 1 warning generated.
100:11.16 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/nsGlobalWindowInner.cpp:20:
100:11.16 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/Crypto.h:10:
100:11.16 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/SubtleCrypto.h:13:
100:11.16 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/CryptoKey.h:12:
100:11.16 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
100:11.16   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
100:11.16       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
100:41.24 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/nsGlobalWindowOuter.cpp:138:
100:41.24 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/Crypto.h:10:
100:41.24 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/SubtleCrypto.h:13:
100:41.24 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/CryptoKey.h:12:
100:41.24 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
100:41.24   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
100:41.24       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
100:53.32 1 warning generated.
100:53.42 netwerk/base
100:56.99 1 warning generated.
100:59.15 In file included from Unified_cpp_netwerk_base0.cpp:11:
100:59.15 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/BackgroundFileSaver.cpp:7:
100:59.15 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/BackgroundFileSaver.h:15:
100:59.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
100:59.15   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
100:59.15       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
101:34.40 1 warning generated.
101:34.50 netwerk/dns
101:34.58 In file included from Unified_cpp_netwerk_base1.cpp:56:
101:34.58 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/SSLTokensCache.cpp:5:
101:34.58 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/SSLTokensCache.h:8:
101:34.58 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/CertVerifier.h:12:
101:34.58 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/EnterpriseRoots.h:10:
101:34.58 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
101:34.58   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
101:34.58       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
101:46.80 1 warning generated.
102:08.07 In file included from Unified_cpp_netwerk_base2.cpp:92:
102:08.07 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsIOService.cpp:61:
102:08.07 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/net/SSLTokensCache.h:8:
102:08.07 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/CertVerifier.h:12:
102:08.07 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/EnterpriseRoots.h:10:
102:08.07 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
102:08.07   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
102:08.07       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
102:20.74 1 warning generated.
102:37.50 In file included from Unified_cpp_netwerk_base3.cpp:38:
102:37.50 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsNetUtil.cpp:83:
102:37.50 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.h:10:
102:37.50 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/nsINSSComponent.h:22:
102:37.50 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/SharedCertVerifier.h:8:
102:37.50 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/CertVerifier.h:12:
102:37.50 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/EnterpriseRoots.h:10:
102:37.50 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
102:37.50   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
102:37.50       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
102:48.86 In file included from Unified_cpp_dom_base1.cpp:65:
102:48.86 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/Crypto.cpp:7:
102:48.86 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/Crypto.h:10:
102:48.86 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/SubtleCrypto.h:13:
102:48.86 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/CryptoKey.h:12:
102:48.87 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
102:48.87   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
102:48.87       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
102:53.46 1 warning generated.
102:58.13 In file included from Unified_cpp_netwerk_base4.cpp:2:
102:58.13 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsSocketTransport2.cpp:15:
102:58.13 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/protocol/http/QuicSocketControl.h:10:
102:58.13 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/CommonSocketControl.h:10:
102:58.13 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/CertVerifier.h:12:
102:58.13 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/EnterpriseRoots.h:10:
102:58.13 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
102:58.13   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
102:58.13       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
103:15.14 1 warning generated.
103:15.25 security/manager/ssl
103:17.55 In file included from Unified_cpp_security_manager_ssl0.cpp:2:
103:17.55 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/AppSignatureVerification.cpp:7:
103:17.55 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSCertificateDB.h:8:
103:17.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
103:17.55   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
103:17.55       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
103:23.43 1 warning generated.
103:23.91 In file included from Unified_cpp_security_manager_ssl1.cpp:2:
103:23.91 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/PKCS11ModuleDB.cpp:9:
103:23.91 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/certverifier/CertVerifier.h:12:
103:23.91 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/EnterpriseRoots.h:10:
103:23.91 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
103:23.91   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
103:23.91       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
103:43.77 1 warning generated.
103:45.44 1 warning generated.
103:45.52 toolkit/components/telemetry
103:46.04 In file included from Unified_cpp_security_manager_ssl2.cpp:11:
103:46.04 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSCertificate.cpp:6:
103:46.04 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSCertificate.h:9:
103:46.04 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
103:46.04   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
103:46.04       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
103:54.28 In file included from Unified_cpp_security_manager_ssl2.cpp:20:
103:54.28 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSCertificateDB.cpp:904:27: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
103:54.28   904 |   if (aInputSpan.Length() > std::numeric_limits<unsigned int>::max()) {
103:54.28       |       ~~~~~~~~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
103:54.41 toolkit/library/buildid.cpp.stub
103:54.42 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
103:54.42 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
103:54.42 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:91:11: error: redefinition of 'end' with a different type: 'char *' vs 'size_t' (aka 'unsigned int')
103:54.42    91 |     char* end = nullptr;
103:54.42       |           ^
103:54.42 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:83:12: note: previous definition is here
103:54.42    83 |     size_t end = token.find_last_not_of(" \t");
103:54.42       |            ^
103:54.42 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:92:53: error: cannot initialize a parameter of type 'char **' with an rvalue of type 'size_t *' (aka 'unsigned int *')
103:54.42    92 |     unsigned long val = std::strtoul(token.c_str(), &end, 16);
103:54.42       |                                                     ^~~~
103:54.42 /usr/include/stdlib.h:221:26: note: passing argument to parameter '__endptr' here
103:54.42   221 |                                           char **__restrict __endptr,
103:54.42       |                                                             ^
103:54.42 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
103:54.42 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
103:54.42 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:27: error: comparison between pointer and integer ('size_t' (aka 'unsigned int') and 'const char *')
103:54.42    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
103:54.42       |                       ~~~ ^  ~~~~~~~~~~~~~
103:54.42 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:47: error: indirection requires pointer operand ('size_t' (aka 'unsigned int') invalid)
103:54.42    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
103:54.42       |                                               ^~~~
103:54.69 toolkit/library
103:57.92 In file included from Unified_cpp_security_manager_ssl3.cpp:2:
103:57.93 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsTLSSocketProvider.cpp:9:
103:57.93 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSIOLayer.h:19:
103:57.93 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSCertificate.h:9:
103:57.93 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
103:57.93   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
103:57.93       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
103:58.33 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
103:58.33 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:1875:21: warning: result of comparison 'size_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
103:58.33  1875 |   if (cert.Length() > std::numeric_limits<uint32_t>::max()) {
103:58.33       |       ~~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
104:08.57 3 warnings and 4 errors generated.
104:08.66 gmake[5]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:676: Unified_cpp_security_manager_ssl2.o] Error 1
104:08.67 gmake[5]: *** Waiting for unfinished jobs....
104:09.37 1 warning generated.
104:09.42 gmake[4]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:72: security/manager/ssl/target-objects] Error 2
104:09.42 gmake[4]: *** Waiting for unfinished jobs....
105:09.57 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/toolkit/components/telemetry/dap/DAPTelemetry.cpp:11:
105:09.57 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/nsNSSComponent.h:10:
105:09.57 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/nsINSSComponent.h:22:
105:09.57 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/SharedCertVerifier.h:8:
105:09.57 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/CertVerifier.h:12:
105:09.57 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/EnterpriseRoots.h:10:
105:09.57 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
105:09.57   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
105:09.57       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
105:13.79 In file included from Unified_cpp_dom_base6.cpp:110:
105:13.79 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/dom/base/SubtleCrypto.cpp:7:
105:13.79 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/SubtleCrypto.h:13:
105:13.79 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-linux-gnu/dist/include/mozilla/dom/CryptoKey.h:12:
105:13.79 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/ScopedNSSTypes.h:283:22: warning: result of comparison 'index_type' (aka 'unsigned int') > 4294967295 is always false [-Wtautological-type-limit-compare]
105:13.79   283 |     if (key.Length() > std::numeric_limits<unsigned int>::max()) {
105:13.79       |         ~~~~~~~~~~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
105:18.29 1 warning generated.
105:28.54 1 warning generated.
106:06.02 gmake[3]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:34: compile] Error 2
106:06.06 gmake[2]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:359: default] Error 2
106:06.10 gmake[1]: *** [client.mk:60: build] Error 2
106:06.20 W 259 compiler warnings present.
106:08.32 W Notification center failed: Install notify-send (usually part of the libnotify package) to get a notification when the build finishes.
 Config object not found by mach.
Configure complete!
Be sure to run |mach build| to pick up any changes
  Parallelism determined by memory: using 4 jobs for 4 cores based on 15.6 GiB RAM and estimated job size of 1.0 GiB
make: *** [Makefile:132: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.


build (windows, x86_64, ubuntu-24.04)
Run python3 ./multibuild.py --target windows --arch x86_64
python3 scripts/patch.py 135.0.1 beta.24 --mozconfig-only
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: downloading component rust-std
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: downloading component rust-std
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-pc-mingw32
-> Updating mozconfig, target is x86_64-pc-mingw32
Complete!
rm -rf camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox-bin \
	camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox
make[1]: Entering directory '/home/runner/work/firefox/firefox'
python3 scripts/patch.py 135.0.1 beta.24
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: component rust-std for target x86_64-pc-windows-gnu is up to date
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: component rust-std for target i686-pc-windows-gnu is up to date
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: x86_64-pc-mingw32
-> Updating mozconfig, target is x86_64-pc-mingw32

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patching file browser/components/asrouter/modules/OnboardingMessageProvider.sys.mjs
Hunk #1 succeeded at 1370 (offset 155 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patching file toolkit/components/extensions/Extension.sys.mjs
Hunk #1 succeeded at 3892 (offset 606 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patching file browser/components/enterprisepolicies/schemas/policies-schema.json
Hunk #1 succeeded at 1385 (offset 311 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patching file gfx/thebes/gfxHarfBuzzShaper.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patching file dom/media/CubebUtils.cpp
Hunk #1 succeeded at 43 (offset 3 lines).
Hunk #2 succeeded at 411 (offset 11 lines).
patching file dom/media/moz.build
patching file dom/media/webaudio/AudioContext.cpp
Hunk #2 succeeded at 556 (offset -6 lines).
Hunk #3 succeeded at 712 (offset -6 lines).
patching file dom/media/webaudio/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patching file python/mozversioncontrol/mozversioncontrol/repo/source.py

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patching file browser/base/content/browser-init.js
Hunk #3 succeeded at 120 with fuzz 2 (offset 1 line).
Hunk #4 succeeded at 320 (offset -16 lines).
Hunk #5 succeeded at 371 (offset -16 lines).
Hunk #6 succeeded at 417 (offset -16 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patching file dom/base/ChromeUtils.cpp
Hunk #2 succeeded at 2416 (offset 299 lines).
Hunk #3 succeeded at 2460 (offset 299 lines).
patching file dom/base/ChromeUtils.h
Hunk #1 succeeded at 315 (offset 10 lines).
Hunk #2 succeeded at 328 (offset 10 lines).
patching file dom/chrome-webidl/ChromeUtils.webidl
Hunk #1 succeeded at 769 (offset 19 lines).
Hunk #2 succeeded at 787 (offset 19 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patching file browser/installer/package-manifest.in
Hunk #1 succeeded at 256 (offset 12 lines).
patching file lw/moz.build
patching file moz.build
Hunk #1 succeeded at 226 with fuzz 1 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patching file browser/base/content/browser-context.inc
Hunk #1 succeeded at 106 (offset -1 lines).
Hunk #2 succeeded at 259 (offset -2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patching file toolkit/components/extensions/parent/ext-storage.js
Hunk #1 succeeded at 403 (offset 226 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patching file toolkit/components/remote/nsDBusRemoteClient.cpp
Hunk #3 succeeded at 121 (offset 4 lines).
Hunk #4 succeeded at 132 (offset 4 lines).
patching file toolkit/components/remote/nsDBusRemoteServer.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patching file devtools/server/actors/thread.js
patching file devtools/server/actors/webconsole/listeners/console-api.js
Hunk #1 succeeded at 97 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patching file browser/moz.configure
patching file python/mach/mach/telemetry.py
Hunk #1 succeeded at 95 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patching file browser/components/extensions/parent/ext-browser.js
patching file browser/components/extensions/parent/ext-tabs.js

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patching file browser/base/content/browser.js
Hunk #1 succeeded at 3399 with fuzz 2 (offset -2079 lines).
patching file browser/components/BrowserGlue.sys.mjs
Hunk #1 succeeded at 1585 with fuzz 2 (offset 311 lines).
patching file browser/components/moz.build
Hunk #1 succeeded at 48 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patching file docshell/base/BrowsingContext.cpp
Hunk #2 succeeded at 1770 (offset -3 lines).
patching file docshell/base/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patching file browser/app/moz.build
patching file dom/base/Element.cpp
Hunk #1 succeeded at 12 with fuzz 2.
Hunk #2 succeeded at 1012 (offset 27 lines).
patching file dom/base/Navigator.cpp
Hunk #6 succeeded at 374 with fuzz 1 (offset -1 lines).
Hunk #7 succeeded at 429 (offset -4 lines).
Hunk #8 succeeded at 452 (offset -10 lines).
Hunk #9 succeeded at 484 (offset -10 lines).
Hunk #10 succeeded at 529 (offset -10 lines).
Hunk #11 succeeded at 570 (offset -10 lines).
Hunk #12 succeeded at 600 (offset -10 lines).
Hunk #13 succeeded at 649 (offset -10 lines).
Hunk #14 succeeded at 665 (offset -10 lines).
Hunk #15 succeeded at 727 (offset -10 lines).
Hunk #16 succeeded at 747 (offset -10 lines).
Hunk #17 succeeded at 762 (offset -10 lines).
Hunk #18 succeeded at 964 (offset -10 lines).
patching file dom/base/moz.build
Hunk #1 succeeded at 659 (offset 18 lines).
patching file dom/base/nsGlobalWindowInner.cpp
Hunk #2 succeeded at 3425 (offset 14 lines).
Hunk #3 succeeded at 3439 (offset 14 lines).
Hunk #4 succeeded at 3458 (offset 14 lines).
Hunk #5 succeeded at 3486 (offset 14 lines).
Hunk #6 succeeded at 3530 (offset 14 lines).
Hunk #7 succeeded at 3604 (offset 14 lines).
patching file dom/base/nsHistory.cpp
patching file dom/base/nsScreen.cpp
Hunk #3 succeeded at 91 with fuzz 1 (offset -3 lines).
patching file dom/battery/BatteryManager.cpp
patching file dom/battery/moz.build
patching file dom/workers/WorkerNavigator.cpp
Hunk #2 succeeded at 104 (offset 11 lines).
Hunk #3 succeeded at 130 (offset 11 lines).
Hunk #4 succeeded at 158 (offset 11 lines).
Hunk #5 succeeded at 224 (offset 7 lines).
Hunk #6 succeeded at 241 (offset 7 lines).
patching file dom/workers/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patching file browser/base/content/navigator-toolbox.inc.xhtml
Hunk #2 succeeded at 663 (offset 4 lines).
patching file browser/components/customizableui/CustomizableUI.sys.mjs
Hunk #1 succeeded at 356 (offset 9 lines).
Hunk #2 succeeded at 715 (offset 9 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patching file gfx/thebes/gfxPlatformFontList.cpp
patching file gfx/thebes/moz.build
Hunk #1 succeeded at 303 (offset -2 lines).
patching file layout/style/FontFace.cpp
Hunk #1 succeeded at 243 (offset 6 lines).
Hunk #2 succeeded at 262 (offset 6 lines).
patching file layout/style/FontFaceImpl.cpp
Hunk #1 succeeded at 358 (offset 1 line).
patching file layout/style/FontFaceImpl.h
Hunk #1 succeeded at 8 with fuzz 2.
Hunk #2 succeeded at 33 (offset -3 lines).
patching file layout/style/moz.build
Hunk #1 succeeded at 366 (offset 15 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patching file layout/style/nsMediaFeatures.cpp
Hunk #1 succeeded at 376 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patching file dom/geolocation/Geolocation.cpp
Hunk #1 succeeded at 39 (offset 5 lines).
Hunk #2 succeeded at 1427 with fuzz 2 (offset 159 lines).
patching file dom/geolocation/GeolocationPosition.cpp
patching file dom/geolocation/moz.build
Hunk #1 succeeded at 81 (offset 23 lines).
patching file dom/system/NetworkGeolocationProvider.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patching file layout/style/GlobalStyleSheetCache.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patching file uriloader/exthandler/HandlerList.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #2 succeeded at 54 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patching file intl/components/src/Locale.cpp
patching file intl/components/src/Locale.h
patching file intl/locale/OSPreferences.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patching file toolkit/xre/nsAppRunner.cpp
Hunk #1 succeeded at 5669 (offset 36 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patching file dom/media/MediaDevices.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patching file toolkit/xre/nsXREDirProvider.cpp
Hunk #1 succeeded at 285 with fuzz 1 (offset -15 lines).
Hunk #2 succeeded at 366 (offset -5 lines).
Hunk #3 succeeded at 398 with fuzz 2 (offset -13 lines).
Hunk #4 succeeded at 932 (offset -182 lines).
Hunk #5 succeeded at 1192 (offset -171 lines).
Hunk #6 succeeded at 1202 (offset -171 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patching file netwerk/protocol/http/moz.build
Hunk #1 succeeded at 234 (offset 16 lines).
patching file netwerk/protocol/http/nsHttpHandler.cpp
Hunk #2 succeeded at 885 (offset 137 lines).
Hunk #3 succeeded at 1997 (offset 149 lines).
Hunk #4 succeeded at 2019 (offset 149 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patching file dom/animation/AnimationEffect.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patching file toolkit/components/search/SearchEngineSelector.sys.mjs
Hunk #1 succeeded at 181 (offset 23 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patching file security/manager/ssl/nsNSSComponent.cpp
Hunk #2 succeeded at 1617 with fuzz 1.
patching file security/manager/ssl/moz.build
Hunk #1 succeeded at 199 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patching file browser/base/content/browser-addons.js
Hunk #1 succeeded at 2393 (offset 469 lines).
patching file browser/base/content/main-popupset.inc.xhtml
Hunk #1 succeeded at 365 (offset 79 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patching file browser/locales/en-US/browser/browser.ftl
Hunk #1 succeeded at 715 (offset 172 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #1 succeeded at 775 (offset 33 lines).
Hunk #2 succeeded at 785 (offset 33 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patching file browser/components/preferences/preferences.js
Hunk #1 succeeded at 241 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patching file browser/extensions/moz.build
patching file browser/locales/Makefile.in
Hunk #1 succeeded at 55 (offset -1 lines).
Hunk #2 succeeded at 75 (offset -2 lines).
patching file browser/locales/filter.py
Hunk #1 succeeded at 15 (offset -2 lines).
patching file browser/locales/l10n.ini
patching file browser/locales/l10n.toml
Hunk #1 succeeded at 135 (offset 2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patching file build/moz.configure/rust.configure

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patching file dom/base/nsScreen.cpp
patching file gfx/src/moz.build
patching file gfx/src/nsDeviceContext.cpp
patching file layout/style/nsMediaFeatures.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patching file dom/webidl/Element.webidl

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patching file browser/components/asrouter/content/asrouter-admin.bundle.js
Hunk #1 succeeded at 1144 with fuzz 1.
patching file services/settings/Utils.sys.mjs
Hunk #1 succeeded at 51 (offset -3 lines).
patching file toolkit/components/search/SearchUtils.sys.mjs
Hunk #1 succeeded at 169 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patching file intl/components/moz.build
patching file intl/components/src/TimeZone.cpp
Hunk #2 succeeded at 22 (offset -1 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patching file browser/components/urlbar/UrlbarProviderInterventions.sys.mjs
Hunk #1 succeeded at 453 (offset -1 lines).
Hunk #2 succeeded at 495 (offset 1 line).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patching file dom/media/webspeech/synth/moz.build
patching file dom/media/webspeech/synth/nsSynthVoiceRegistry.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patching file dom/canvas/ClientWebGLContext.cpp
Hunk #2 succeeded at 754 (offset 1 line).
Hunk #3 succeeded at 771 (offset 1 line).
Hunk #4 succeeded at 1022 (offset 1 line).
Hunk #5 succeeded at 2112 (offset 1 line).
Hunk #6 succeeded at 2268 (offset 1 line).
Hunk #7 succeeded at 2525 (offset 1 line).
Hunk #8 succeeded at 2538 (offset 1 line).
Hunk #9 succeeded at 2635 (offset 2 lines).
Hunk #10 succeeded at 3020 (offset 2 lines).
Hunk #11 succeeded at 6018 (offset 2 lines).
Hunk #12 succeeded at 6040 (offset 2 lines).
patching file dom/canvas/ClientWebGLContext.h
Hunk #1 succeeded at 1073 (offset -1 lines).
patching file dom/canvas/moz.build
Hunk #1 succeeded at 228 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.cpp
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.h
patching file dom/media/webrtc/jsapi/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patching file browser/app/Makefile.in
patching file browser/app/camoufox.exe.manifest (renamed from browser/app/firefox.exe.manifest)

--- Applied 48 patch(es) successfully ---
Complete!
touch camoufox-135.0.1-beta.24/_READY
make[1]: Leaving directory '/home/runner/work/firefox/firefox'
cd camoufox-135.0.1-beta.24 && ./mach build 
Collecting glean-sdk==63.0.0
  Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl.metadata (4.8 kB)
Collecting semver>=2.13.0 (from glean-sdk==63.0.0)
  Downloading semver-3.0.4-py3-none-any.whl.metadata (6.8 kB)
Requirement already satisfied: glean-parser~=16.1 in ./third_party/python/glean_parser (from glean-sdk==63.0.0) (16.1.0)
Requirement already satisfied: Click>=7 in ./third_party/python/click (from glean-parser~=16.1->glean-sdk==63.0.0) (8.1.6)
Requirement already satisfied: diskcache>=4 in ./third_party/python/diskcache (from glean-parser~=16.1->glean-sdk==63.0.0) (5.6.3)
Requirement already satisfied: Jinja2>=2.10.1 in ./third_party/python/Jinja2 (from glean-parser~=16.1->glean-sdk==63.0.0) (3.1.2)
Requirement already satisfied: jsonschema>=3.0.2 in ./third_party/python/jsonschema (from glean-parser~=16.1->glean-sdk==63.0.0) (4.17.3)
Requirement already satisfied: platformdirs>=2.4.0 in ./third_party/python/platformdirs (from glean-parser~=16.1->glean-sdk==63.0.0) (4.3.6)
Requirement already satisfied: PyYAML>=5.3.1 in ./third_party/python/PyYAML/lib (from glean-parser~=16.1->glean-sdk==63.0.0) (6.0.1)
Requirement already satisfied: MarkupSafe>=2.0 in ./third_party/python/MarkupSafe/src (from Jinja2>=2.10.1->glean-parser~=16.1->glean-sdk==63.0.0) (2.0.1)
Requirement already satisfied: attrs>=17.4.0 in ./third_party/python/attrs (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (23.1.0)
Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in ./third_party/python/pyrsistent (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (0.20.0)
Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl (861 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 861.6/861.6 kB 20.5 MB/s eta 0:00:00
Downloading semver-3.0.4-py3-none-any.whl (17 kB)
Installing collected packages: semver, glean-sdk
Successfully installed glean-sdk-63.0.0 semver-3.0.4
Collecting psutil<=5.9.4,>=5.4.2
  Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (21 kB)
Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (280 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 280.2/280.2 kB 12.7 MB/s eta 0:00:00
Installing collected packages: psutil
Successfully installed psutil-5.9.4
Collecting zstandard<=0.23.0,>=0.11.1
  Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (3.0 kB)
Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 28.7 MB/s eta 0:00:00
Installing collected packages: zstandard
Successfully installed zstandard-0.23.0
Mach and the build system store shared state in a common directory
on the filesystem. The following directory will be created:

  /home/runner/.mozbuild

If you would like to use a different directory, rename or move it to your
desired location, and set the MOZBUILD_STATE_PATH environment variable
accordingly.
Creating default state directory: /home/runner/.mozbuild
Creating local state directory: /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7
 0:00.80 W Clobber not needed.
 0:00.99 Using Python 3.11.15 from /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python
 0:00.99 Adding configure options from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/mozconfig
 0:00.99   --enable-application=browser
 0:00.99   --allow-addon-sideload
 0:00.99   --disable-crashreporter
 0:00.99   --disable-backgroundtasks
 0:00.99   --disable-debug
 0:00.99   --disable-default-browser-agent
 0:00.99   --disable-tests
 0:00.99   --disable-updater
 0:00.99   --enable-release
 0:00.99   --disable-system-policies
 0:00.99   --without-wasm-sandboxed-libraries
 0:00.99   --with-app-name=camoufox
 0:00.99   --with-branding=browser/branding/camoufox
 0:00.99   --with-unsigned-addon-scopes=app,system
 0:00.99   --disable-bootstrap
 0:00.99   --with-libclang-path=/usr/lib/llvm-18/lib
 0:00.99   --target=x86_64-pc-mingw32
 0:00.99   --disable-maintenance-service
 0:00.99   --disable-update-agent
 0:00.99   --disable-accessibility
 0:00.99   RC=x86_64-w64-mingw32-windres
 0:00.99   MOZ_REQUIRE_SIGNING=
 0:00.99   AR=x86_64-w64-mingw32-ar
 0:00.99   CC=clang --target=x86_64-w64-mingw32
 0:00.99   CXX=clang++ --target=x86_64-w64-mingw32
 0:00.99   WINDRES=x86_64-w64-mingw32-windres
 0:00.99   LIBCLANG_PATH=/usr/lib/llvm-18/lib
 0:00.99   RANLIB=x86_64-w64-mingw32-ranlib
 0:00.99   LLVM_DLLTOOL=llvm-dlltool-18
 0:00.99   MINGW_TRIPLE=x86_64-w64-mingw32
 0:00.99 checking for vcs source checkout... no
 0:01.04 checking for a shell... /usr/bin/sh
 0:01.07 checking for host system type... x86_64-pc-linux-gnu
 0:01.08 checking for target system type... x86_64-pc-mingw32
 0:01.33 checking whether cross compiling... yes
 0:01.40 checking for Python 3... /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python (3.11.15)
 0:01.40 checking for wget... /usr/bin/wget
 0:01.40 checking for ccache... not found
 0:01.40 checking for the target C compiler... /usr/bin/clang
 0:01.46 checking whether the target C compiler can be used... yes
 0:01.46 checking the target C compiler version... 18.1.8
 0:01.49 checking the target C compiler works... yes
 0:01.49 checking for the target C++ compiler... /usr/bin/clang++
 0:01.53 checking whether the target C++ compiler can be used... yes
 0:01.53 checking the target C++ compiler version... 18.1.8
 0:01.55 checking the target C++ compiler works... yes
 0:01.55 checking for the host C compiler... /usr/bin/clang
 0:01.57 checking whether the host C compiler can be used... yes
 0:01.57 checking the host C compiler version... 18.1.8
 0:01.60 checking the host C compiler works... yes
 0:01.60 checking for the host C++ compiler... /usr/bin/clang++
 0:01.63 checking whether the host C++ compiler can be used... yes
 0:01.64 checking the host C++ compiler version... 18.1.8
 0:01.66 checking the host C++ compiler works... yes
 0:01.69 checking for host linker... lld
 0:01.76 checking for 64-bit OS... yes
 0:01.79 checking for new enough STL headers from libstdc++... yes
 0:01.85 checking for __thread keyword for TLS variables... yes
 0:01.85 checking for Windows SDK... no
 0:01.85 checking for Universal CRT SDK... no
 0:01.86 checking for linker... /usr/bin/lld-link
 0:01.88 checking for w32api version >= 3.14... yes
 0:01.88 checking for the assembler... /usr/bin/clang
 0:01.90 checking for llvm-objdump... /usr/bin/llvm-objdump
 0:01.90 checking for rc... /usr/bin/x86_64-w64-mingw32-windres
 0:01.92 checking for ar... /usr/bin/x86_64-w64-mingw32-ar
 0:01.95 checking whether ar supports response files... no
 0:01.96 checking for host_ar... /usr/bin/llvm-ar
 0:02.01 checking for -mavxvnni support... yes
 0:02.03 checking for -mavx512bw support... yes
 0:02.05 checking for -mavx512vnni support... yes
 0:02.09 checking for malloc.h... yes
 0:02.11 checking for stdint.h... yes
 0:02.14 checking for inttypes.h... yes
 0:02.16 checking for alloca.h... no
 0:02.18 checking for sys/byteorder.h... no
 0:02.21 checking for getopt.h... yes
 0:02.24 checking for unistd.h... yes
 0:02.26 checking for nl_types.h... no
 0:02.28 checking for cpuid.h... yes
 0:02.30 checking for fts.h... no
 0:02.33 checking for sys/statvfs.h... no
 0:02.35 checking for sys/statfs.h... no
 0:02.37 checking for sys/vfs.h... no
 0:02.39 checking for sys/mount.h... no
 0:02.41 checking for sys/quota.h... no
 0:02.43 checking for sys/queue.h... no
 0:02.45 checking for sys/types.h... yes
 0:02.48 checking for netinet/in.h... no
 0:02.50 checking for byteswap.h... no
 0:02.52 checking for memfd_create in sys/mman.h... no
 0:02.58 checking for clock_gettime(CLOCK_MONOTONIC)... no
 0:02.64 checking for clock_gettime(CLOCK_MONOTONIC) in rt... no
 0:02.68 checking for res_ninit()... no
 0:02.73 checking for dladdr... no
 0:02.78 checking for dladdr in -ldl... no
 0:02.81 checking for dlfcn.h... no
 0:02.86 checking for dlopen in -ldl... no
 0:02.91 checking for dlopen... no
 0:02.97 checking for gethostbyname_r in -lc_r... no
 0:03.02 checking for socket in -lsocket... no
 0:03.07 checking for pthread_create... no
 0:03.14 checking for pthread_create in -lpthread... yes
 0:03.17 checking for pthread.h... yes
 0:03.19 checking whether the C compiler supports -pthread... yes
 0:03.29 checking whether 64-bits std::atomic requires -latomic... no
 0:03.31 checking whether the C compiler supports -Wbitfield-enum-conversion... yes
 0:03.34 checking whether the C++ compiler supports -Wbitfield-enum-conversion... yes
 0:03.36 checking whether the C compiler supports -Wformat-type-confusion... yes
 0:03.38 checking whether the C++ compiler supports -Wformat-type-confusion... yes
 0:03.40 checking whether the C compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.43 checking whether the C++ compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.45 checking whether the C compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.47 checking whether the C++ compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.50 checking whether the C compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.52 checking whether the C++ compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.54 checking whether the C compiler supports -Wunreachable-code-return... yes
 0:03.57 checking whether the C++ compiler supports -Wunreachable-code-return... yes
 0:03.59 checking whether the C compiler supports -Wunused-but-set-parameter... yes
 0:03.61 checking whether the C++ compiler supports -Wunused-but-set-parameter... yes
 0:03.63 checking whether the C compiler supports -Wclass-varargs... yes
 0:03.66 checking whether the C++ compiler supports -Wclass-varargs... yes
 0:03.68 checking whether the C++ compiler supports -Wempty-init-stmt... yes
 0:03.70 checking whether the C compiler supports -Wfloat-overflow-conversion... yes
 0:03.73 checking whether the C++ compiler supports -Wfloat-overflow-conversion... yes
 0:03.75 checking whether the C compiler supports -Wfloat-zero-conversion... yes
 0:03.77 checking whether the C++ compiler supports -Wfloat-zero-conversion... yes
 0:03.80 checking whether the C compiler supports -Wloop-analysis... yes
 0:03.82 checking whether the C++ compiler supports -Wloop-analysis... yes
 0:03.84 checking whether the C compiler supports -Wno-range-loop-analysis... yes
 0:03.87 checking whether the C++ compiler supports -Wno-range-loop-analysis... yes
 0:03.89 checking whether the C++ compiler supports -Wcomma-subscript... no
 0:03.91 checking whether the C compiler supports -Wenum-compare-conditional... yes
 0:03.93 checking whether the C++ compiler supports -Wenum-compare-conditional... yes
 0:03.96 checking whether the C compiler supports -Wenum-float-conversion... yes
 0:03.98 checking whether the C++ compiler supports -Wenum-float-conversion... yes
 0:04.00 checking whether the C++ compiler supports -Wvolatile... no
 0:04.02 checking whether the C++ compiler supports -Wno-deprecated-anon-enum-enum-conversion... yes
 0:04.05 checking whether the C++ compiler supports -Wno-deprecated-enum-enum-conversion... yes
 0:04.07 checking whether the C++ compiler supports -Wno-deprecated-this-capture... yes
 0:04.09 checking whether the C++ compiler supports -Wcomma... yes
 0:04.11 checking whether the C compiler supports -Wduplicated-cond... no
 0:04.13 checking whether the C++ compiler supports -Wduplicated-cond... no
 0:04.15 checking whether the C++ compiler supports -Wimplicit-fallthrough... yes
 0:04.17 checking whether the C compiler supports -Wlogical-op... no
 0:04.19 checking whether the C++ compiler supports -Wlogical-op... no
 0:04.22 checking whether the C compiler supports -Wstring-conversion... yes
 0:04.24 checking whether the C++ compiler supports -Wstring-conversion... yes
 0:04.27 checking whether the C++ compiler supports -Wno-inline-new-delete... yes
 0:04.29 checking whether the C compiler supports -Wno-error=maybe-uninitialized... no
 0:04.31 checking whether the C++ compiler supports -Wno-error=maybe-uninitialized... no
 0:04.33 checking whether the C compiler supports -Wno-error=deprecated-declarations... yes
 0:04.35 checking whether the C++ compiler supports -Wno-error=deprecated-declarations... yes
 0:04.38 checking whether the C compiler supports -Wno-error=array-bounds... yes
 0:04.40 checking whether the C++ compiler supports -Wno-error=array-bounds... yes
 0:04.42 checking whether the C compiler supports -Wno-error=free-nonheap-object... yes
 0:04.45 checking whether the C++ compiler supports -Wno-error=free-nonheap-object... yes
 0:04.47 checking whether the C compiler supports -Wno-multistatement-macros... no
 0:04.49 checking whether the C++ compiler supports -Wno-multistatement-macros... no
 0:04.51 checking whether the C compiler supports -Wno-error=class-memaccess... no
 0:04.53 checking whether the C++ compiler supports -Wno-error=class-memaccess... no
 0:04.55 checking whether the C compiler supports -Wno-error=atomic-alignment... yes
 0:04.57 checking whether the C++ compiler supports -Wno-error=atomic-alignment... yes
 0:04.59 checking whether the C compiler supports -Wno-error=deprecated-builtins... yes
 0:04.62 checking whether the C++ compiler supports -Wno-error=deprecated-builtins... yes
 0:04.64 checking whether the C compiler supports -Wno-unknown-pragmas... yes
 0:04.67 checking whether the C++ compiler supports -Wno-unknown-pragmas... yes
 0:04.69 checking whether the C compiler supports -Wno-unused-function... yes
 0:04.72 checking whether the C++ compiler supports -Wno-unused-function... yes
 0:04.74 checking whether the C compiler supports -Wno-conversion-null... yes
 0:04.76 checking whether the C++ compiler supports -Wno-conversion-null... yes
 0:04.79 checking whether the C compiler supports -Wno-switch... yes
 0:04.81 checking whether the C++ compiler supports -Wno-switch... yes
 0:04.83 checking whether the C compiler supports -Wno-enum-compare... yes
 0:04.86 checking whether the C++ compiler supports -Wno-enum-compare... yes
 0:04.88 checking whether the C compiler supports -Werror=implicit-function-declaration... yes
 0:04.90 checking whether the C compiler supports -Wno-psabi... yes
 0:04.93 checking whether the C++ compiler supports -Wno-psabi... yes
 0:04.95 checking whether the C compiler supports -Wthread-safety... yes
 0:04.97 checking whether the C++ compiler supports -Wthread-safety... yes
 0:05.00 checking whether the C compiler supports -Wno-error=builtin-macro-redefined... yes
 0:05.02 checking whether the C++ compiler supports -Wno-error=builtin-macro-redefined... yes
 0:05.04 checking whether the C++ compiler supports -Wno-vla-cxx-extension... yes
 0:05.07 checking whether the C compiler supports -Wno-unknown-warning-option... yes
 0:05.09 checking whether the C++ compiler supports -Wno-unknown-warning-option... yes
 0:05.11 checking whether the C++ compiler supports -fno-sized-deallocation... yes
 0:05.14 checking whether the C++ compiler supports -fno-aligned-new... yes
 0:05.18 checking whether the linker supports Identical Code Folding... no
 0:05.24 checking whether the C linker supports -Wl,--build-id=sha1... yes
 0:05.26 checking whether the C assembler supports -Wa,--noexecstack... yes
 0:05.31 checking whether the C linker supports -Wl,-z,noexecstack... no
 0:05.35 checking whether the C linker supports -Wl,-z,text... no
 0:05.39 checking whether the C linker supports -Wl,-z,relro... no
 0:05.43 checking whether the C linker supports -Wl,-z,now... no
 0:05.47 checking whether the C linker supports -Wl,-z,nocopyreloc... no
 0:05.53 checking what kind of list files are supported by the linker... linkerlist
 0:05.53 checking for llvm_profdata... not found
 0:05.57 checking for readelf... /usr/bin/llvm-readelf
 0:05.60 checking for objcopy... /usr/bin/llvm-objcopy
 0:05.60 checking for rustc... /home/runner/.cargo/bin/rustc
 0:05.60 checking for cargo... /home/runner/.cargo/bin/cargo
 0:05.76 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc'
 0:06.23 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/cargo'
 0:06.24 checking rustc version... 1.94.1
 0:06.29 checking cargo version... 1.94.1
 0:09.35 checking for rust host triplet... x86_64-unknown-linux-gnu
 0:09.73 checking for rust target triplet... x86_64-pc-windows-gnu
 0:09.73 checking for rustdoc... /home/runner/.cargo/bin/rustdoc
 0:09.73 checking for cbindgen... /usr/bin/cbindgen
 0:09.73 checking for rustfmt... /home/runner/.cargo/bin/rustfmt
 0:09.73 checking for clang for bindgen... /usr/bin/clang++
 0:09.73 checking for libclang for bindgen... /usr/lib/llvm-18/lib/libclang.so
 0:09.74 checking that libclang is new enough... yes
 0:09.74 checking bindgen cflags... -x c++ -fno-sized-deallocation -fno-aligned-new -DTRACING=1 -DIMPL_LIBXUL -DMOZILLA_INTERNAL_API -DRUST_BINDGEN -DWIN32=1 --target=x86_64-w64-mingw32
 0:09.77 checking for tm_zone and tm_gmtoff in struct tm... no
 0:09.83 checking for _getc_nolock... yes
 0:09.89 checking for localeconv... yes
 0:10.58 checking for nodejs... /usr/local/bin/node (20.20.2)
 0:10.58 checking for tar... /usr/bin/tar
 0:10.58 checking for unzip... /usr/bin/unzip
 0:10.58 checking for the Mozilla API key... no
 0:10.58 checking for the Google Location Service API key... no
 0:10.58 checking for the Google Safebrowsing API key... no
 0:10.58 checking for the Bing API key... no
 0:10.58 checking for the Adjust SDK key... no
 0:10.58 checking for the Leanplum SDK key... no
 0:10.58 checking for the Pocket API key... no
 0:10.58 checking for midl... not found
 0:10.59 checking for llvm-dlltool... /usr/bin/llvm-dlltool-18
 0:10.59 checking for fxc... not found
 0:10.59 DEBUG: fxc: Looking for fxc.exe
 0:10.59 DEBUG: fxc: Looking for fxc2.exe
 0:10.59 ERROR: Cannot find fxc
 0:10.66 W Exception when writing resource usage file: [Errno 2] No such file or directory: '/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-x86_64-pc-mingw32/.mozbuild/profile_build_resources.json'
 Config object not found by mach.
*** Fix above errors and then restart with "./mach build"
make: *** [Makefile:132: build] Error 1

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.

build (windows, i686, ubuntu-24.04)
Run python3 ./multibuild.py --target windows --arch i686
python3 scripts/patch.py 135.0.1 beta.24 --mozconfig-only
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: downloading component rust-std
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: downloading component rust-std
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: i686-pc-mingw32
-> Updating mozconfig, target is i686-pc-mingw32
Complete!
rm -rf camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox-bin \
	camoufox-135.0.1-beta.24/obj-x86_64-pc-linux-gnu/dist/bin/camoufox
make[1]: Entering directory '/home/runner/work/firefox/firefox'
python3 scripts/patch.py 135.0.1 beta.24
~/.cargo/bin/rustup target add "x86_64-pc-windows-gnu"
info: component rust-std for target x86_64-pc-windows-gnu is up to date
~/.cargo/bin/rustup target add "i686-pc-windows-gnu"
info: component rust-std for target i686-pc-windows-gnu is up to date
cp -v ../assets/base.mozconfig mozconfig
'../assets/base.mozconfig' -> 'mozconfig'
Using target: i686-pc-mingw32
-> Updating mozconfig, target is i686-pc-mingw32

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/ghostery/Disable-Onboarding-Messages.patch
patching file browser/components/asrouter/modules/OnboardingMessageProvider.sys.mjs
Hunk #1 succeeded at 1370 (offset 155 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/all-addons-private-mode.patch
patching file toolkit/components/extensions/Extension.sys.mjs
Hunk #1 succeeded at 3892 (offset 606 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/allow-searchengines-non-esr.patch
patching file browser/components/enterprisepolicies/schemas/policies-schema.json
Hunk #1 succeeded at 1385 (offset 311 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/anti-font-fingerprinting.patch
patching file gfx/thebes/gfxHarfBuzzShaper.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/audio-context-spoofing.patch
patching file dom/media/CubebUtils.cpp
Hunk #1 succeeded at 43 (offset 3 lines).
Hunk #2 succeeded at 411 (offset 11 lines).
patching file dom/media/moz.build
patching file dom/media/webaudio/AudioContext.cpp
Hunk #2 succeeded at 556 (offset -6 lines).
Hunk #3 succeeded at 712 (offset -6 lines).
patching file dom/media/webaudio/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/bootstrap.patch
patching file python/mozversioncontrol/mozversioncontrol/repo/source.py

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/browser-init.patch
patching file browser/base/content/browser-init.js
Hunk #3 succeeded at 120 with fuzz 2 (offset 1 line).
Hunk #4 succeeded at 320 (offset -16 lines).
Hunk #5 succeeded at 371 (offset -16 lines).
Hunk #6 succeeded at 417 (offset -16 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/chromeutil.patch
patching file dom/base/ChromeUtils.cpp
Hunk #2 succeeded at 2416 (offset 299 lines).
Hunk #3 succeeded at 2460 (offset 299 lines).
patching file dom/base/ChromeUtils.h
Hunk #1 succeeded at 315 (offset 10 lines).
Hunk #2 succeeded at 328 (offset 10 lines).
patching file dom/chrome-webidl/ChromeUtils.webidl
Hunk #1 succeeded at 769 (offset 19 lines).
Hunk #2 succeeded at 787 (offset 19 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/config.patch
patching file browser/installer/package-manifest.in
Hunk #1 succeeded at 256 (offset 12 lines).
patching file lw/moz.build
patching file moz.build
Hunk #1 succeeded at 226 with fuzz 1 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/context-menu.patch
patching file browser/base/content/browser-context.inc
Hunk #1 succeeded at 106 (offset -1 lines).
Hunk #2 succeeded at 259 (offset -2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/custom-ubo-assets-bootstrap-location.patch
patching file toolkit/components/extensions/parent/ext-storage.js
Hunk #1 succeeded at 403 (offset 226 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/dbus_name.patch
patching file toolkit/components/remote/nsDBusRemoteClient.cpp
Hunk #3 succeeded at 121 (offset 4 lines).
Hunk #4 succeeded at 132 (offset 4 lines).
patching file toolkit/components/remote/nsDBusRemoteServer.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/devtools-bypass.patch
patching file devtools/server/actors/thread.js
patching file devtools/server/actors/webconsole/listeners/console-api.js
Hunk #1 succeeded at 97 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/disable-data-reporting-at-compile-time.patch
patching file browser/moz.configure
patching file python/mach/mach/telemetry.py
Hunk #1 succeeded at 95 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/disable-extension-newtab.patch
patching file browser/components/extensions/parent/ext-browser.js
patching file browser/components/extensions/parent/ext-tabs.js

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/disable-pocket.patch
patching file browser/base/content/browser.js
Hunk #1 succeeded at 3399 with fuzz 2 (offset -2079 lines).
patching file browser/components/BrowserGlue.sys.mjs
Hunk #1 succeeded at 1585 with fuzz 2 (offset 311 lines).
patching file browser/components/moz.build
Hunk #1 succeeded at 48 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/disable-remote-subframes.patch
patching file docshell/base/BrowsingContext.cpp
Hunk #2 succeeded at 1770 (offset -3 lines).
patching file docshell/base/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/fingerprint-injection.patch
patching file browser/app/moz.build
patching file dom/base/Element.cpp
Hunk #1 succeeded at 12 with fuzz 2.
Hunk #2 succeeded at 1012 (offset 27 lines).
patching file dom/base/Navigator.cpp
Hunk #6 succeeded at 374 with fuzz 1 (offset -1 lines).
Hunk #7 succeeded at 429 (offset -4 lines).
Hunk #8 succeeded at 452 (offset -10 lines).
Hunk #9 succeeded at 484 (offset -10 lines).
Hunk #10 succeeded at 529 (offset -10 lines).
Hunk #11 succeeded at 570 (offset -10 lines).
Hunk #12 succeeded at 600 (offset -10 lines).
Hunk #13 succeeded at 649 (offset -10 lines).
Hunk #14 succeeded at 665 (offset -10 lines).
Hunk #15 succeeded at 727 (offset -10 lines).
Hunk #16 succeeded at 747 (offset -10 lines).
Hunk #17 succeeded at 762 (offset -10 lines).
Hunk #18 succeeded at 964 (offset -10 lines).
patching file dom/base/moz.build
Hunk #1 succeeded at 659 (offset 18 lines).
patching file dom/base/nsGlobalWindowInner.cpp
Hunk #2 succeeded at 3425 (offset 14 lines).
Hunk #3 succeeded at 3439 (offset 14 lines).
Hunk #4 succeeded at 3458 (offset 14 lines).
Hunk #5 succeeded at 3486 (offset 14 lines).
Hunk #6 succeeded at 3530 (offset 14 lines).
Hunk #7 succeeded at 3604 (offset 14 lines).
patching file dom/base/nsHistory.cpp
patching file dom/base/nsScreen.cpp
Hunk #3 succeeded at 91 with fuzz 1 (offset -3 lines).
patching file dom/battery/BatteryManager.cpp
patching file dom/battery/moz.build
patching file dom/workers/WorkerNavigator.cpp
Hunk #2 succeeded at 104 (offset 11 lines).
Hunk #3 succeeded at 130 (offset 11 lines).
Hunk #4 succeeded at 158 (offset 11 lines).
Hunk #5 succeeded at 224 (offset 7 lines).
Hunk #6 succeeded at 241 (offset 7 lines).
patching file dom/workers/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/firefox-view.patch
patching file browser/base/content/navigator-toolbox.inc.xhtml
Hunk #2 succeeded at 663 (offset 4 lines).
patching file browser/components/customizableui/CustomizableUI.sys.mjs
Hunk #1 succeeded at 356 (offset 9 lines).
Hunk #2 succeeded at 715 (offset 9 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/font-hijacker.patch
patching file gfx/thebes/gfxPlatformFontList.cpp
patching file gfx/thebes/moz.build
Hunk #1 succeeded at 303 (offset -2 lines).
patching file layout/style/FontFace.cpp
Hunk #1 succeeded at 243 (offset 6 lines).
Hunk #2 succeeded at 262 (offset 6 lines).
patching file layout/style/FontFaceImpl.cpp
Hunk #1 succeeded at 358 (offset 1 line).
patching file layout/style/FontFaceImpl.h
Hunk #1 succeeded at 8 with fuzz 2.
Hunk #2 succeeded at 33 (offset -3 lines).
patching file layout/style/moz.build
Hunk #1 succeeded at 366 (offset 15 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/force-default-pointer.patch
patching file layout/style/nsMediaFeatures.cpp
Hunk #1 succeeded at 376 (offset 4 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/geolocation-spoofing.patch
patching file dom/geolocation/Geolocation.cpp
Hunk #1 succeeded at 39 (offset 5 lines).
Hunk #2 succeeded at 1427 with fuzz 2 (offset 159 lines).
patching file dom/geolocation/GeolocationPosition.cpp
patching file dom/geolocation/moz.build
Hunk #1 succeeded at 81 (offset 23 lines).
patching file dom/system/NetworkGeolocationProvider.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/global-style-sheets.patch
patching file layout/style/GlobalStyleSheetCache.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/handlers.patch
patching file uriloader/exthandler/HandlerList.sys.mjs

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/hide-default-browser.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #2 succeeded at 54 (offset 6 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/locale-spoofing.patch
patching file intl/components/src/Locale.cpp
patching file intl/components/src/Locale.h
patching file intl/locale/OSPreferences.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/macos-backgroundtasks-disabled.patch
patching file toolkit/xre/nsAppRunner.cpp
Hunk #1 succeeded at 5669 (offset 36 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/media-device-spoofing.patch
patching file dom/media/MediaDevices.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/mozilla_dirs.patch
patching file toolkit/xre/nsXREDirProvider.cpp
Hunk #1 succeeded at 285 with fuzz 1 (offset -15 lines).
Hunk #2 succeeded at 366 (offset -5 lines).
Hunk #3 succeeded at 398 with fuzz 2 (offset -13 lines).
Hunk #4 succeeded at 932 (offset -182 lines).
Hunk #5 succeeded at 1192 (offset -171 lines).
Hunk #6 succeeded at 1202 (offset -171 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/network-patches.patch
patching file netwerk/protocol/http/moz.build
Hunk #1 succeeded at 234 (offset 16 lines).
patching file netwerk/protocol/http/nsHttpHandler.cpp
Hunk #2 succeeded at 885 (offset 137 lines).
Hunk #3 succeeded at 1997 (offset 149 lines).
Hunk #4 succeeded at 2019 (offset 149 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-css-animations.patch
patching file dom/animation/AnimationEffect.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/no-search-engines.patch
patching file toolkit/components/search/SearchEngineSelector.sys.mjs
Hunk #1 succeeded at 181 (offset 23 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/nss-tls-override.patch
patching file security/manager/ssl/nsNSSComponent.cpp
Hunk #2 succeeded at 1617 with fuzz 1.
patching file security/manager/ssl/moz.build
Hunk #1 succeeded at 199 with fuzz 1.

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/pin-addons.patch
patching file browser/base/content/browser-addons.js
Hunk #1 succeeded at 2393 (offset 469 lines).
patching file browser/base/content/main-popupset.inc.xhtml
Hunk #1 succeeded at 365 (offset 79 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-branding-urlbar.patch
patching file browser/locales/en-US/browser/browser.ftl
Hunk #1 succeeded at 715 (offset 172 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-cfrprefs.patch
patching file browser/components/preferences/main.inc.xhtml
Hunk #1 succeeded at 775 (offset 33 lines).
Hunk #2 succeeded at 785 (offset 33 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/ui-patches/remove-organization-policy-banner.patch
patching file browser/components/preferences/preferences.js
Hunk #1 succeeded at 241 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/remove_addons.patch
patching file browser/extensions/moz.build
patching file browser/locales/Makefile.in
Hunk #1 succeeded at 55 (offset -1 lines).
Hunk #2 succeeded at 75 (offset -2 lines).
patching file browser/locales/filter.py
Hunk #1 succeeded at 15 (offset -2 lines).
patching file browser/locales/l10n.ini
patching file browser/locales/l10n.toml
Hunk #1 succeeded at 135 (offset 2 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/rust-gentoo-musl.patch
patching file build/moz.configure/rust.configure

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/screen-hijacker.patch
patching file dom/base/nsScreen.cpp
patching file gfx/src/moz.build
patching file gfx/src/nsDeviceContext.cpp
patching file layout/style/nsMediaFeatures.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/shadow-root-bypass.patch
patching file dom/webidl/Element.webidl

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/sed-patches/stop-undesired-requests.patch
patching file browser/components/asrouter/content/asrouter-admin.bundle.js
Hunk #1 succeeded at 1144 with fuzz 1.
patching file services/settings/Utils.sys.mjs
Hunk #1 succeeded at 51 (offset -3 lines).
patching file toolkit/components/search/SearchUtils.sys.mjs
Hunk #1 succeeded at 169 (offset -3 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/identity/timezone-spoofing.patch
patching file intl/components/moz.build
patching file intl/components/src/TimeZone.cpp
Hunk #2 succeeded at 22 (offset -1 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/librewolf/urlbarprovider-interventions.patch
patching file browser/components/urlbar/UrlbarProviderInterventions.sys.mjs
Hunk #1 succeeded at 453 (offset -1 lines).
Hunk #2 succeeded at 495 (offset 1 line).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/security/voice-spoofing.patch
patching file dom/media/webspeech/synth/moz.build
patching file dom/media/webspeech/synth/nsSynthVoiceRegistry.cpp

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/media/webgl-spoofing.patch
patching file dom/canvas/ClientWebGLContext.cpp
Hunk #2 succeeded at 754 (offset 1 line).
Hunk #3 succeeded at 771 (offset 1 line).
Hunk #4 succeeded at 1022 (offset 1 line).
Hunk #5 succeeded at 2112 (offset 1 line).
Hunk #6 succeeded at 2268 (offset 1 line).
Hunk #7 succeeded at 2525 (offset 1 line).
Hunk #8 succeeded at 2538 (offset 1 line).
Hunk #9 succeeded at 2635 (offset 2 lines).
Hunk #10 succeeded at 3020 (offset 2 lines).
Hunk #11 succeeded at 6018 (offset 2 lines).
Hunk #12 succeeded at 6040 (offset 2 lines).
patching file dom/canvas/ClientWebGLContext.h
Hunk #1 succeeded at 1073 (offset -1 lines).
patching file dom/canvas/moz.build
Hunk #1 succeeded at 228 (offset 7 lines).

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/network/webrtc-ip-spoofing.patch
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.cpp
patching file dom/media/webrtc/jsapi/PeerConnectionImpl.h
patching file dom/media/webrtc/jsapi/moz.build

*** -> patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patch -p1 -i /home/runner/work/firefox/firefox/patches/core/windows-theming-bug-modified.patch
patching file browser/app/Makefile.in
patching file browser/app/camoufox.exe.manifest (renamed from browser/app/firefox.exe.manifest)

--- Applied 48 patch(es) successfully ---
Complete!
touch camoufox-135.0.1-beta.24/_READY
make[1]: Leaving directory '/home/runner/work/firefox/firefox'
cd camoufox-135.0.1-beta.24 && ./mach build 
Collecting glean-sdk==63.0.0
  Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl.metadata (4.8 kB)
Collecting semver>=2.13.0 (from glean-sdk==63.0.0)
  Downloading semver-3.0.4-py3-none-any.whl.metadata (6.8 kB)
Requirement already satisfied: glean-parser~=16.1 in ./third_party/python/glean_parser (from glean-sdk==63.0.0) (16.1.0)
Requirement already satisfied: Click>=7 in ./third_party/python/click (from glean-parser~=16.1->glean-sdk==63.0.0) (8.1.6)
Requirement already satisfied: diskcache>=4 in ./third_party/python/diskcache (from glean-parser~=16.1->glean-sdk==63.0.0) (5.6.3)
Requirement already satisfied: Jinja2>=2.10.1 in ./third_party/python/Jinja2 (from glean-parser~=16.1->glean-sdk==63.0.0) (3.1.2)
Requirement already satisfied: jsonschema>=3.0.2 in ./third_party/python/jsonschema (from glean-parser~=16.1->glean-sdk==63.0.0) (4.17.3)
Requirement already satisfied: platformdirs>=2.4.0 in ./third_party/python/platformdirs (from glean-parser~=16.1->glean-sdk==63.0.0) (4.3.6)
Requirement already satisfied: PyYAML>=5.3.1 in ./third_party/python/PyYAML/lib (from glean-parser~=16.1->glean-sdk==63.0.0) (6.0.1)
Requirement already satisfied: MarkupSafe>=2.0 in ./third_party/python/MarkupSafe/src (from Jinja2>=2.10.1->glean-parser~=16.1->glean-sdk==63.0.0) (2.0.1)
Requirement already satisfied: attrs>=17.4.0 in ./third_party/python/attrs (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (23.1.0)
Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in ./third_party/python/pyrsistent (from jsonschema>=3.0.2->glean-parser~=16.1->glean-sdk==63.0.0) (0.20.0)
Downloading glean_sdk-63.0.0-py3-none-manylinux_2_34_x86_64.whl (861 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 861.6/861.6 kB 23.1 MB/s eta 0:00:00
Downloading semver-3.0.4-py3-none-any.whl (17 kB)
Installing collected packages: semver, glean-sdk
Successfully installed glean-sdk-63.0.0 semver-3.0.4
Collecting psutil<=5.9.4,>=5.4.2
  Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (21 kB)
Downloading psutil-5.9.4-cp36-abi3-manylinux_2_12_x86_64.manylinux2010_x86_64.manylinux_2_17_x86_64.manylinux2014_x86_64.whl (280 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 280.2/280.2 kB 15.1 MB/s eta 0:00:00
Installing collected packages: psutil
Successfully installed psutil-5.9.4
Collecting zstandard<=0.23.0,>=0.11.1
  Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (3.0 kB)
Downloading zstandard-0.23.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (5.4 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.4/5.4 MB 27.8 MB/s eta 0:00:00
Installing collected packages: zstandard
Successfully installed zstandard-0.23.0
Mach and the build system store shared state in a common directory
on the filesystem. The following directory will be created:

  /home/runner/.mozbuild

If you would like to use a different directory, rename or move it to your
desired location, and set the MOZBUILD_STATE_PATH environment variable
accordingly.
Creating default state directory: /home/runner/.mozbuild
Creating local state directory: /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7
 0:00.80 W Clobber not needed.
 0:00.99 Using Python 3.11.15 from /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python
 0:00.99 Adding configure options from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/mozconfig
 0:00.99   --enable-application=browser
 0:00.99   --allow-addon-sideload
 0:00.99   --disable-crashreporter
 0:00.99   --disable-backgroundtasks
 0:00.99   --disable-debug
 0:00.99   --disable-default-browser-agent
 0:00.99   --disable-tests
 0:00.99   --disable-updater
 0:00.99   --enable-release
 0:00.99   --disable-system-policies
 0:00.99   --without-wasm-sandboxed-libraries
 0:00.99   --with-app-name=camoufox
 0:00.99   --with-branding=browser/branding/camoufox
 0:00.99   --with-unsigned-addon-scopes=app,system
 0:00.99   --disable-bootstrap
 0:00.99   --with-libclang-path=/usr/lib/llvm-18/lib
 0:00.99   --target=i686-pc-mingw32
 0:00.99   --disable-maintenance-service
 0:00.99   --disable-update-agent
 0:00.99   --disable-accessibility
 0:00.99   CC=clang --target=i686-w64-mingw32
 0:00.99   WINDRES=i686-w64-mingw32-windres
 0:00.99   LLVM_DLLTOOL=llvm-dlltool-18
 0:00.99   LIBCLANG_PATH=/usr/lib/llvm-18/lib
 0:00.99   CXX=clang++ --target=i686-w64-mingw32
 0:00.99   RC=i686-w64-mingw32-windres
 0:00.99   MOZ_REQUIRE_SIGNING=
 0:00.99   AR=i686-w64-mingw32-ar
 0:00.99   RANLIB=i686-w64-mingw32-ranlib
 0:00.99   MINGW_TRIPLE=i686-w64-mingw32
 0:00.99 checking for vcs source checkout... no
 0:01.04 checking for a shell... /usr/bin/sh
 0:01.07 checking for host system type... x86_64-pc-linux-gnu
 0:01.07 checking for target system type... i686-pc-mingw32
 0:01.30 checking whether cross compiling... yes
 0:01.37 checking for Python 3... /home/runner/.mozbuild/srcdirs/camoufox-135.0.1-beta.24-05492dc3a9e7/_virtualenvs/build/bin/python (3.11.15)
 0:01.37 checking for wget... /usr/bin/wget
 0:01.38 checking for ccache... not found
 0:01.38 checking for the target C compiler... /usr/bin/clang
 0:01.43 checking whether the target C compiler can be used... yes
 0:01.43 checking the target C compiler version... 18.1.8
 0:01.45 checking the target C compiler works... yes
 0:01.45 checking for the target C++ compiler... /usr/bin/clang++
 0:01.49 checking whether the target C++ compiler can be used... yes
 0:01.49 checking the target C++ compiler version... 18.1.8
 0:01.51 checking the target C++ compiler works... yes
 0:01.51 checking for the host C compiler... /usr/bin/clang
 0:01.53 checking whether the host C compiler can be used... yes
 0:01.53 checking the host C compiler version... 18.1.8
 0:01.55 checking the host C compiler works... yes
 0:01.55 checking for the host C++ compiler... /usr/bin/clang++
 0:01.58 checking whether the host C++ compiler can be used... yes
 0:01.58 checking the host C++ compiler version... 18.1.8
 0:01.61 checking the host C++ compiler works... yes
 0:01.63 checking for host linker... lld
 0:01.69 checking for 64-bit OS... no
 0:01.72 checking for new enough STL headers from libstdc++... yes
 0:01.78 checking for __thread keyword for TLS variables... yes
 0:01.78 checking for Windows SDK... no
 0:01.78 checking for Universal CRT SDK... no
 0:01.78 checking for linker... /usr/bin/lld-link
 0:01.80 checking for w32api version >= 3.14... yes
 0:01.80 checking for the assembler... /usr/bin/clang
 0:01.82 checking for llvm-objdump... /usr/bin/llvm-objdump
 0:01.82 checking for rc... /usr/bin/i686-w64-mingw32-windres
 0:01.84 checking for ar... /usr/bin/i686-w64-mingw32-ar
 0:01.86 checking whether ar supports response files... no
 0:01.88 checking for host_ar... /usr/bin/llvm-ar
 0:01.92 checking for -mavxvnni support... yes
 0:01.94 checking for -mavx512bw support... yes
 0:01.96 checking for -mavx512vnni support... yes
 0:01.99 checking for malloc.h... yes
 0:02.01 checking for stdint.h... yes
 0:02.03 checking for inttypes.h... yes
 0:02.05 checking for alloca.h... no
 0:02.07 checking for sys/byteorder.h... no
 0:02.10 checking for getopt.h... yes
 0:02.12 checking for unistd.h... yes
 0:02.14 checking for nl_types.h... no
 0:02.16 checking for cpuid.h... yes
 0:02.18 checking for fts.h... no
 0:02.20 checking for sys/statvfs.h... no
 0:02.22 checking for sys/statfs.h... no
 0:02.24 checking for sys/vfs.h... no
 0:02.26 checking for sys/mount.h... no
 0:02.28 checking for sys/quota.h... no
 0:02.30 checking for sys/queue.h... no
 0:02.32 checking for sys/types.h... yes
 0:02.34 checking for netinet/in.h... no
 0:02.36 checking for byteswap.h... no
 0:02.38 checking for memfd_create in sys/mman.h... no
 0:02.43 checking for clock_gettime(CLOCK_MONOTONIC)... no
 0:02.49 checking for clock_gettime(CLOCK_MONOTONIC) in rt... no
 0:02.52 checking for res_ninit()... no
 0:02.58 checking for dladdr... no
 0:02.63 checking for dladdr in -ldl... no
 0:02.64 checking for dlfcn.h... no
 0:02.69 checking for dlopen in -ldl... no
 0:02.74 checking for dlopen... no
 0:02.79 checking for gethostbyname_r in -lc_r... no
 0:02.84 checking for socket in -lsocket... no
 0:02.89 checking for pthread_create... no
 0:02.95 checking for pthread_create in -lpthread... yes
 0:02.98 checking for pthread.h... yes
 0:03.00 checking whether the C compiler supports -pthread... yes
 0:03.09 checking whether 64-bits std::atomic requires -latomic... no
 0:03.11 checking whether the C compiler supports -Wbitfield-enum-conversion... yes
 0:03.13 checking whether the C++ compiler supports -Wbitfield-enum-conversion... yes
 0:03.16 checking whether the C compiler supports -Wformat-type-confusion... yes
 0:03.18 checking whether the C++ compiler supports -Wformat-type-confusion... yes
 0:03.20 checking whether the C compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.22 checking whether the C++ compiler supports -Wshadow-field-in-constructor-modified... yes
 0:03.24 checking whether the C compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.26 checking whether the C++ compiler supports -Wtautological-constant-in-range-compare... yes
 0:03.28 checking whether the C compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.31 checking whether the C++ compiler supports -Wno-error=tautological-type-limit-compare... yes
 0:03.33 checking whether the C compiler supports -Wunreachable-code-return... yes
 0:03.35 checking whether the C++ compiler supports -Wunreachable-code-return... yes
 0:03.37 checking whether the C compiler supports -Wunused-but-set-parameter... yes
 0:03.39 checking whether the C++ compiler supports -Wunused-but-set-parameter... yes
 0:03.41 checking whether the C compiler supports -Wclass-varargs... yes
 0:03.43 checking whether the C++ compiler supports -Wclass-varargs... yes
 0:03.45 checking whether the C++ compiler supports -Wempty-init-stmt... yes
 0:03.48 checking whether the C compiler supports -Wfloat-overflow-conversion... yes
 0:03.50 checking whether the C++ compiler supports -Wfloat-overflow-conversion... yes
 0:03.52 checking whether the C compiler supports -Wfloat-zero-conversion... yes
 0:03.54 checking whether the C++ compiler supports -Wfloat-zero-conversion... yes
 0:03.56 checking whether the C compiler supports -Wloop-analysis... yes
 0:03.58 checking whether the C++ compiler supports -Wloop-analysis... yes
 0:03.60 checking whether the C compiler supports -Wno-range-loop-analysis... yes
 0:03.62 checking whether the C++ compiler supports -Wno-range-loop-analysis... yes
 0:03.64 checking whether the C++ compiler supports -Wcomma-subscript... no
 0:03.66 checking whether the C compiler supports -Wenum-compare-conditional... yes
 0:03.68 checking whether the C++ compiler supports -Wenum-compare-conditional... yes
 0:03.70 checking whether the C compiler supports -Wenum-float-conversion... yes
 0:03.72 checking whether the C++ compiler supports -Wenum-float-conversion... yes
 0:03.74 checking whether the C++ compiler supports -Wvolatile... no
 0:03.76 checking whether the C++ compiler supports -Wno-deprecated-anon-enum-enum-conversion... yes
 0:03.78 checking whether the C++ compiler supports -Wno-deprecated-enum-enum-conversion... yes
 0:03.80 checking whether the C++ compiler supports -Wno-deprecated-this-capture... yes
 0:03.82 checking whether the C++ compiler supports -Wcomma... yes
 0:03.84 checking whether the C compiler supports -Wduplicated-cond... no
 0:03.86 checking whether the C++ compiler supports -Wduplicated-cond... no
 0:03.88 checking whether the C++ compiler supports -Wimplicit-fallthrough... yes
 0:03.90 checking whether the C compiler supports -Wlogical-op... no
 0:03.92 checking whether the C++ compiler supports -Wlogical-op... no
 0:03.94 checking whether the C compiler supports -Wstring-conversion... yes
 0:03.96 checking whether the C++ compiler supports -Wstring-conversion... yes
 0:03.98 checking whether the C++ compiler supports -Wno-inline-new-delete... yes
 0:04.00 checking whether the C compiler supports -Wno-error=maybe-uninitialized... no
 0:04.02 checking whether the C++ compiler supports -Wno-error=maybe-uninitialized... no
 0:04.04 checking whether the C compiler supports -Wno-error=deprecated-declarations... yes
 0:04.06 checking whether the C++ compiler supports -Wno-error=deprecated-declarations... yes
 0:04.08 checking whether the C compiler supports -Wno-error=array-bounds... yes
 0:04.10 checking whether the C++ compiler supports -Wno-error=array-bounds... yes
 0:04.12 checking whether the C compiler supports -Wno-error=free-nonheap-object... yes
 0:04.14 checking whether the C++ compiler supports -Wno-error=free-nonheap-object... yes
 0:04.16 checking whether the C compiler supports -Wno-multistatement-macros... no
 0:04.18 checking whether the C++ compiler supports -Wno-multistatement-macros... no
 0:04.20 checking whether the C compiler supports -Wno-error=class-memaccess... no
 0:04.22 checking whether the C++ compiler supports -Wno-error=class-memaccess... no
 0:04.24 checking whether the C compiler supports -Wno-error=atomic-alignment... yes
 0:04.26 checking whether the C++ compiler supports -Wno-error=atomic-alignment... yes
 0:04.28 checking whether the C compiler supports -Wno-error=deprecated-builtins... yes
 0:04.30 checking whether the C++ compiler supports -Wno-error=deprecated-builtins... yes
 0:04.32 checking whether the C compiler supports -Wno-unknown-pragmas... yes
 0:04.34 checking whether the C++ compiler supports -Wno-unknown-pragmas... yes
 0:04.37 checking whether the C compiler supports -Wno-unused-function... yes
 0:04.39 checking whether the C++ compiler supports -Wno-unused-function... yes
 0:04.41 checking whether the C compiler supports -Wno-conversion-null... yes
 0:04.43 checking whether the C++ compiler supports -Wno-conversion-null... yes
 0:04.45 checking whether the C compiler supports -Wno-switch... yes
 0:04.47 checking whether the C++ compiler supports -Wno-switch... yes
 0:04.49 checking whether the C compiler supports -Wno-enum-compare... yes
 0:04.51 checking whether the C++ compiler supports -Wno-enum-compare... yes
 0:04.53 checking whether the C compiler supports -Werror=implicit-function-declaration... yes
 0:04.55 checking whether the C compiler supports -Wno-psabi... yes
 0:04.58 checking whether the C++ compiler supports -Wno-psabi... yes
 0:04.60 checking whether the C compiler supports -Wthread-safety... yes
 0:04.62 checking whether the C++ compiler supports -Wthread-safety... yes
 0:04.64 checking whether the C compiler supports -Wno-error=builtin-macro-redefined... yes
 0:04.66 checking whether the C++ compiler supports -Wno-error=builtin-macro-redefined... yes
 0:04.68 checking whether the C++ compiler supports -Wno-vla-cxx-extension... yes
 0:04.70 checking whether the C compiler supports -Wno-unknown-warning-option... yes
 0:04.72 checking whether the C++ compiler supports -Wno-unknown-warning-option... yes
 0:04.75 checking whether the C++ compiler supports -fno-sized-deallocation... yes
 0:04.77 checking whether the C++ compiler supports -fno-aligned-new... yes
 0:04.81 checking whether the linker supports Identical Code Folding... no
 0:04.86 checking whether the C linker supports -Wl,--build-id=sha1... yes
 0:04.88 checking whether the C assembler supports -Wa,--noexecstack... yes
 0:04.92 checking whether the C linker supports -Wl,-z,noexecstack... no
 0:04.96 checking whether the C linker supports -Wl,-z,text... no
 0:04.99 checking whether the C linker supports -Wl,-z,relro... no
 0:05.03 checking whether the C linker supports -Wl,-z,now... no
 0:05.07 checking whether the C linker supports -Wl,-z,nocopyreloc... no
 0:05.12 checking what kind of list files are supported by the linker... linkerlist
 0:05.12 checking for llvm_profdata... not found
 0:05.16 checking for readelf... /usr/bin/llvm-readelf
 0:05.18 checking for objcopy... /usr/bin/llvm-objcopy
 0:05.19 checking for rustc... /home/runner/.cargo/bin/rustc
 0:05.19 checking for cargo... /home/runner/.cargo/bin/cargo
 0:05.33 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/rustc'
 0:05.96 Actually using '/home/runner/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/bin/cargo'
 0:05.97 checking rustc version... 1.94.1
 0:06.09 checking cargo version... 1.94.1
 0:09.45 checking for rust host triplet... x86_64-unknown-linux-gnu
 0:09.92 checking for rust target triplet... i686-pc-windows-gnu
 0:09.92 checking for rustdoc... /home/runner/.cargo/bin/rustdoc
 0:09.92 checking for cbindgen... /usr/bin/cbindgen
 0:09.92 checking for rustfmt... /home/runner/.cargo/bin/rustfmt
 0:09.92 checking for clang for bindgen... /usr/bin/clang++
 0:09.92 checking for libclang for bindgen... /usr/lib/llvm-18/lib/libclang.so
 0:09.94 checking that libclang is new enough... yes
 0:09.94 checking bindgen cflags... -x c++ -fno-sized-deallocation -fno-aligned-new -DTRACING=1 -DIMPL_LIBXUL -DMOZILLA_INTERNAL_API -DRUST_BINDGEN -DWIN32=1 --target=i686-w64-mingw32
 0:09.96 checking for tm_zone and tm_gmtoff in struct tm... no
 0:10.02 checking for _getc_nolock... yes
 0:10.08 checking for localeconv... yes
 0:10.82 checking for nodejs... /usr/local/bin/node (20.20.2)
 0:10.82 checking for tar... /usr/bin/tar
 0:10.82 checking for unzip... /usr/bin/unzip
 0:10.83 checking for the Mozilla API key... no
 0:10.83 checking for the Google Location Service API key... no
 0:10.83 checking for the Google Safebrowsing API key... no
 0:10.83 checking for the Bing API key... no
 0:10.83 checking for the Adjust SDK key... no
 0:10.83 checking for the Leanplum SDK key... no
 0:10.83 checking for the Pocket API key... no
 0:10.83 checking for midl... not found
 0:10.83 checking for llvm-dlltool... /usr/bin/llvm-dlltool-18
 0:10.83 checking for fxc... not found
 0:10.83 DEBUG: fxc: Looking for fxc.exe
 0:10.83 DEBUG: fxc: Looking for fxc2.exe
 0:10.83 ERROR: Cannot find fxc
 0:10.89 W Exception when writing resource usage file: [Errno 2] No such file or directory: '/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-i686-pc-mingw32/.mozbuild/profile_build_resources.json'
 Config object not found by mach.
*** Fix above errors and then restart with "./mach build"
make: *** [Makefile:132: build] Error 1

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.

build (macos, x86_64, ubuntu-24.04)
…… 
87:35.33   430 | GetProcessInformation(
87:35.33       | ^
87:35.33 In file included from Unified_mm_widget_cocoa0.mm:137:
87:35.33 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaUtils.mm:289:11: warning: 'GetProcessInformation' is deprecated: first deprecated in macOS 10.9 [-Wdeprecated-declarations]
87:35.33   289 |     if (::GetProcessInformation(&processInfoRec.processLauncher,
87:35.33       |           ^
87:35.33 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/ApplicationServices.framework/Frameworks/HIServices.framework/Headers/Processes.h:430:1: note: 'GetProcessInformation' has been explicitly marked deprecated here
87:35.33   430 | GetProcessInformation(
87:35.33       | ^
87:41.25 In file included from Unified_mm_xpcom_base0.mm:11:
87:41.25 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/base/MacStringHelpers.mm:24:11: warning: result of comparison 'NSUInteger' (aka 'unsigned long') > 18446744073709551615 is always false [-Wtautological-type-limit-compare]
87:41.25    24 |   if (len > std::numeric_limits<nsAString::size_type>::max()) {
87:41.25       |       ~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
87:42.41 1 warning generated.
87:47.55 3 warnings generated.
87:57.13 In file included from Unified_mm_widget_cocoa1.mm:2:
87:57.13 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaWindow.mm:1576:11: warning: 'NSDisableScreenUpdates' is deprecated: first deprecated in macOS 10.11 - As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSDisableScreenUpdates. [-Wdeprecated-declarations]
87:57.13  1576 |           NSDisableScreenUpdates();
87:57.13       |           ^
87:57.13 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h:235:20: note: 'NSDisableScreenUpdates' has been explicitly marked deprecated here
87:57.13   235 | APPKIT_EXTERN void NSDisableScreenUpdates(void) API_DEPRECATED("As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSDisableScreenUpdates.", macos(10.0,10.11));
87:57.13       |                    ^
87:57.13 In file included from Unified_mm_widget_cocoa1.mm:2:
88:18.13   302 | enum {
88:18.13       | ^
88:18.13 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.13 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:508:31: warning: 'kClassicDomain' is deprecated: first deprecated in macOS 10.5 - Deprecated [-Wdeprecated-declarations]
88:18.13   508 |       return GetOSXFolderType(kClassicDomain, kSystemFolderType, aFile);
88:18.13       |                               ^
88:18.13 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:75:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:75:1)' has been explicitly marked deprecated here
88:18.13    75 | enum {
88:18.13       | ^
88:18.13 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.13 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:508:47: warning: 'kSystemFolderType' is deprecated: first deprecated in macOS 10.5 - Deprecated [-Wdeprecated-declarations]
88:18.13   508 |       return GetOSXFolderType(kClassicDomain, kSystemFolderType, aFile);
88:18.13       |                                               ^
88:18.13 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:450:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:450:1)' has been explicitly marked deprecated here
88:18.13   450 | enum {
88:18.13       | ^
88:18.13 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.13 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:511:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.13   511 |       return GetOSXFolderType(kUserDomain, kDomainLibraryFolderType, aFile);
88:18.13       |                               ^
88:18.13 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.13    63 | enum {
88:18.13       | ^
88:18.13 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.13 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:511:44: warning: 'kDomainLibraryFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.13   511 |       return GetOSXFolderType(kUserDomain, kDomainLibraryFolderType, aFile);
88:18.13       |                                            ^
88:18.13 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
88:18.13   302 | enum {
88:18.13       | ^
88:18.13 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:514:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   514 |       return GetOSXFolderType(kUserDomain, kDomainTopLevelFolderType, aFile);
88:18.14       |                               ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.14    63 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:514:44: warning: 'kDomainTopLevelFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   514 |       return GetOSXFolderType(kUserDomain, kDomainTopLevelFolderType, aFile);
88:18.14       |                                            ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
88:18.14   302 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:517:38: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   517 |       nsresult rv = GetOSXFolderType(kUserDomain, kDownloadsFolderType, aFile);
88:18.14       |                                      ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.14    63 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:517:51: warning: 'kDownloadsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   517 |       nsresult rv = GetOSXFolderType(kUserDomain, kDownloadsFolderType, aFile);
88:18.14       |                                                   ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:371:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:371:1)' has been explicitly marked deprecated here
88:18.14   371 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:519:33: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   519 |         return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
88:18.14       |                                 ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.14    63 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:519:46: warning: 'kDesktopFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   519 |         return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
88:18.14       |                                              ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
88:18.14   302 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:524:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   524 |       return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
88:18.14       |                               ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.14    63 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:524:44: warning: 'kDesktopFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   524 |       return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
88:18.14       |                                            ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
88:18.14   302 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:527:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   527 |       return GetOSXFolderType(kUserDomain, kDocumentsFolderType, aFile);
88:18.14       |                               ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.14    63 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:527:44: warning: 'kDocumentsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.14   527 |       return GetOSXFolderType(kUserDomain, kDocumentsFolderType, aFile);
88:18.14       |                                            ^
88:18.14 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1)' has been explicitly marked deprecated here
88:18.14   341 | enum {
88:18.14       | ^
88:18.14 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:530:31: warning: 'kLocalDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   530 |       return GetOSXFolderType(kLocalDomain, kApplicationsFolderType, aFile);
88:18.15       |                               ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.15    63 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:530:45: warning: 'kApplicationsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   530 |       return GetOSXFolderType(kLocalDomain, kApplicationsFolderType, aFile);
88:18.15       |                                             ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
88:18.15   302 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:533:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   533 |       return GetOSXFolderType(kUserDomain, kPreferencesFolderType, aFile);
88:18.15       |                               ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.15    63 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:533:44: warning: 'kPreferencesFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   533 |       return GetOSXFolderType(kUserDomain, kPreferencesFolderType, aFile);
88:18.15       |                                            ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
88:18.15   302 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:536:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   536 |       return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType, aFile);
88:18.15       |                               ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.15    63 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:536:44: warning: 'kPictureDocumentsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   536 |       return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType, aFile);
88:18.15       |                                            ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1)' has been explicitly marked deprecated here
88:18.15   341 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:544:33: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   544 |         return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType,
88:18.15       |                                 ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
88:18.15    63 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:544:46: warning: 'kPictureDocumentsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   544 |         return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType,
88:18.15       |                                              ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1)' has been explicitly marked deprecated here
88:18.15   341 | enum {
88:18.15       | ^
88:18.15 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:706:22: warning: 'kTemporaryFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.15   706 |   if (aFolderType == kTemporaryFolderType) {
88:18.15       |                      ^
88:18.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
88:18.15   302 | enum {
88:18.15       | ^
88:18.16 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.16 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:716:11: warning: 'FSFindFolder' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
88:18.16   716 |   err = ::FSFindFolder(aDomain, aFolderType, kCreateFolder, &fsRef);
88:18.16       |           ^
88:18.16 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:289:1: note: 'FSFindFolder' has been explicitly marked deprecated here
88:18.16   289 | FSFindFolder(
88:18.16       | ^
88:18.16 In file included from Unified_cpp_xpcom_io0.cpp:101:
88:18.16 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:716:46: warning: 'kCreateFolder' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
88:18.16   716 |   err = ::FSFindFolder(aDomain, aFolderType, kCreateFolder, &fsRef);
88:18.16       |                                              ^
88:18.16 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:87:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:87:1)' has been explicitly marked deprecated here
88:18.16    87 | enum {
88:18.16       | ^
88:21.30 xpcom/reflect/xptcall
88:22.15 1 warning generated.
88:24.04 xpcom/reflect/xptinfo
88:24.11 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.11 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1994:36: warning: 'kLSRequestAllInfo' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
88:24.11  1994 |   LSRequestedInfo theInfoRequest = kLSRequestAllInfo;
88:24.11       |                                    ^
88:24.11 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:36:3: note: 'kLSRequestAllInfo' has been explicitly marked deprecated here
88:24.11    36 |   kLSRequestAllInfo                                     __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.") = (UInt32)0xFFFFFFFF /* thread-safe in 10.2*/
88:24.11       |   ^
88:24.11 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.12 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1995:3: warning: 'LSItemInfoRecord' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
88:24.12  1995 |   LSItemInfoRecord theInfo;
88:24.12       |   ^
88:24.12 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:67:3: note: 'LSItemInfoRecord' has been explicitly marked deprecated here
88:24.12    67 | } LSItemInfoRecord __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.");
88:24.12       |   ^
88:24.12 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.12 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1996:23: warning: 'LSCopyItemInfoForURL' is deprecated: first deprecated in macOS 10.11 - Use URL resource properties instead. [-Wdeprecated-declarations]
88:24.12  1996 |   OSStatus result = ::LSCopyItemInfoForURL(url, theInfoRequest, &theInfo);
88:24.12       |                       ^
88:24.12 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:103:1: note: 'LSCopyItemInfoForURL' has been explicitly marked deprecated here
88:24.12   103 | LSCopyItemInfoForURL(
88:24.12       | ^
88:24.12 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.12 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1999:26: warning: 'kLSItemInfoIsApplication' is deprecated: first deprecated in macOS 10.11 - Use the URL resource property kCFURLIsApplicationKey or NSURLIsApplicationKey instead. [-Wdeprecated-declarations]
88:24.12  1999 |     if ((theInfo.flags & kLSItemInfoIsApplication) != 0) {
88:24.12       |                          ^
88:24.12 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:44:3: note: 'kLSItemInfoIsApplication' has been explicitly marked deprecated here
88:24.12    44 |   kLSItemInfoIsApplication                      __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use the URL resource property kCFURLIsApplicationKey or NSURLIsApplicationKey instead.") = 0x00000004, /* Single-file or packaged application*/
88:24.12       |   ^
88:24.14 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.14 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2325:25: warning: 'GetAliasSizeFromPtr' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
88:24.15  2325 |   int32_t aliasSize = ::GetAliasSizeFromPtr(&aliasHeader);
88:24.15       |                         ^
88:24.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Aliases.h:676:1: note: 'GetAliasSizeFromPtr' has been explicitly marked deprecated here
88:24.15   676 | GetAliasSizeFromPtr(const AliasRecord * alias)                __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_4, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
88:24.15       | ^
88:24.15 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2338:9: warning: 'PtrToHand' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
88:24.15  2338 |   if (::PtrToHand(decodedData, &newHandle, aliasSize) != noErr) {
88:24.15       |         ^
88:24.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/MacMemory.h:1773:1: note: 'PtrToHand' has been explicitly marked deprecated here
88:24.15  1773 | PtrToHand(
88:24.15       | ^
88:24.15 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2348:17: warning: 'FSResolveAlias' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
88:24.15  2348 |   OSErr err = ::FSResolveAlias(nullptr, (AliasHandle)newHandle, &resolvedFSRef,
88:24.15       |                 ^
88:24.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Aliases.h:260:1: note: 'FSResolveAlias' has been explicitly marked deprecated here
88:24.15   260 | FSResolveAlias(
88:24.15       | ^
88:24.15 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2352:3: warning: 'DisposeHandle' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
88:24.15  2352 |   DisposeHandle(newHandle);
88:24.15       |   ^
88:24.15 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/MacMemory.h:1279:1: note: 'DisposeHandle' has been explicitly marked deprecated here
88:24.15  1279 | DisposeHandle(Handle h)                                       __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
88:24.15       | ^
88:24.17 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.17 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2728:26: warning: 'CFURLCreateFromFSRef' is deprecated: first deprecated in macOS 10.9 - Not supported [-Wdeprecated-declarations]
88:24.17  2728 |   CFURLRef newURLRef = ::CFURLCreateFromFSRef(kCFAllocatorDefault, aFSRef);
88:24.17       |                          ^
88:24.17 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreFoundation.framework/Headers/CFURL.h:484:10: note: 'CFURLCreateFromFSRef' has been explicitly marked deprecated here
88:24.18   484 | CFURLRef CFURLCreateFromFSRef(CFAllocatorRef allocator, const struct FSRef *fsRef) API_DEPRECATED("Not supported", macos(10.0,10.9), ios(2.0,7.0), watchos(2.0,2.0), tvos(9.0,9.0));
88:24.18       |          ^
88:24.18 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.18 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2760:11: warning: 'CFURLGetFSRef' is deprecated: first deprecated in macOS 10.9 - Not supported [-Wdeprecated-declarations]
88:24.18  2760 |     if (::CFURLGetFSRef(url, aResult)) {
88:24.18       |           ^
88:24.18 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreFoundation.framework/Headers/CFURL.h:487:9: note: 'CFURLGetFSRef' has been explicitly marked deprecated here
88:24.18   487 | Boolean CFURLGetFSRef(CFURLRef url, struct FSRef *fsRef) API_DEPRECATED("Not supported", macos(10.0,10.9), ios(2.0,7.0), watchos(2.0,2.0), tvos(9.0,9.0));
88:24.18       |         ^
88:24.18 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.18 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2778:19: warning: 'FSGetCatalogInfo' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
88:24.18  2778 |     OSErr err = ::FSGetCatalogInfo(&fsRef, kFSCatInfoNone, nullptr, nullptr,
88:24.18       |                   ^
88:24.18 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:2620:15: note: 'FSGetCatalogInfo' has been explicitly marked deprecated here
88:24.18  2620 | extern OSErr  FSGetCatalogInfo(const FSRef *ref, FSCatalogInfoBitmap whichInfo, FSCatalogInfo *catalogInfo, HFSUniStr255 *outName, FSSpecPtr fsSpec, FSRef *parentRef) __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
88:24.18       |               ^
88:24.18 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.18 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2800:9: warning: 'FSGetCatalogInfo' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
88:24.18  2800 |       ::FSGetCatalogInfo(&fsRef, kFSCatInfoDataSizes + kFSCatInfoRsrcSizes,
88:24.18       |         ^
88:24.18 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:2620:15: note: 'FSGetCatalogInfo' has been explicitly marked deprecated here
88:24.19  2620 | extern OSErr  FSGetCatalogInfo(const FSRef *ref, FSCatalogInfoBitmap whichInfo, FSCatalogInfo *catalogInfo, HFSUniStr255 *outName, FSSpecPtr fsSpec, FSRef *parentRef) __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
88:24.19       |               ^
88:24.19 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.19 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2881:3: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
88:24.19  2881 |   LSLaunchFSRefSpec thelaunchSpec;
88:24.19       |   ^
88:24.19 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
88:24.19    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
88:24.19       |   ^
88:24.19 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.19 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2886:36: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
88:24.19  2886 |   memset(&thelaunchSpec, 0, sizeof(LSLaunchFSRefSpec));
88:24.19       |                                    ^
88:24.19 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
88:24.19    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
88:24.19       |   ^
88:24.19 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.19 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2895:17: warning: 'LSOpenFromRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSOpenFromURLSpec or NSWorkspace instead. [-Wdeprecated-declarations]
88:24.20  2895 |   OSErr err = ::LSOpenFromRefSpec(&thelaunchSpec, nullptr);
88:24.20       |                 ^
88:24.20 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:123:1: note: 'LSOpenFromRefSpec' has been explicitly marked deprecated here
88:24.20   123 | LSOpenFromRefSpec(
88:24.20       | ^
88:24.20 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.20 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2912:19: warning: 'LSOpenFSRef' is deprecated: first deprecated in macOS 10.10 - Use LSOpenCFURLRef or -[NSWorkspace openURL:] instead. [-Wdeprecated-declarations]
88:24.20  2912 |     OSErr err = ::LSOpenFSRef(&docFSRef, nullptr);
88:24.20       |                   ^
88:24.20 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:86:1: note: 'LSOpenFSRef' has been explicitly marked deprecated here
88:24.20    86 | LSOpenFSRef(
88:24.20       | ^
88:24.20 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.20 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2937:3: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
88:24.20  2937 |   LSLaunchFSRefSpec thelaunchSpec;
88:24.20       |   ^
88:24.20 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
88:24.20    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
88:24.20       |   ^
88:24.20 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.20 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2942:36: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
88:24.20  2942 |   memset(&thelaunchSpec, 0, sizeof(LSLaunchFSRefSpec));
88:24.20       |                                    ^
88:24.20 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
88:24.20    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
88:24.20       |   ^
88:24.20 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.20 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2949:17: warning: 'LSOpenFromRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSOpenFromURLSpec or NSWorkspace instead. [-Wdeprecated-declarations]
88:24.20  2949 |   OSErr err = ::LSOpenFromRefSpec(&thelaunchSpec, nullptr);
88:24.20       |                 ^
88:24.20 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:123:1: note: 'LSOpenFromRefSpec' has been explicitly marked deprecated here
88:24.20   123 | LSOpenFromRefSpec(
88:24.20       | ^
88:24.20 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.21 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2970:3: warning: 'LSItemInfoRecord' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
88:24.21  2970 |   LSItemInfoRecord info;
88:24.21       |   ^
88:24.21 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:67:3: note: 'LSItemInfoRecord' has been explicitly marked deprecated here
88:24.21    67 | } LSItemInfoRecord __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.");
88:24.21       |   ^
88:24.21 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.21 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2972:9: warning: 'LSCopyItemInfoForURL' is deprecated: first deprecated in macOS 10.11 - Use URL resource properties instead. [-Wdeprecated-declarations]
88:24.21  2972 |       ::LSCopyItemInfoForURL(url, kLSRequestBasicFlagsOnly, &info);
88:24.21       |         ^
88:24.21 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:103:1: note: 'LSCopyItemInfoForURL' has been explicitly marked deprecated here
88:24.21   103 | LSCopyItemInfoForURL(
88:24.21       | ^
88:24.21 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.21 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2972:35: warning: 'kLSRequestBasicFlagsOnly' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
88:24.21  2972 |       ::LSCopyItemInfoForURL(url, kLSRequestBasicFlagsOnly, &info);
88:24.21       |                                   ^
88:24.21 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:31:3: note: 'kLSRequestBasicFlagsOnly' has been explicitly marked deprecated here
88:24.21    31 |   kLSRequestBasicFlagsOnly                      __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.") = 0x00000004, /* thread-safe in 10.2*/
88:24.21       |   ^
88:24.21 In file included from Unified_cpp_xpcom_io1.cpp:47:
88:24.21 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2980:30: warning: 'kLSItemInfoIsPackage' is deprecated: first deprecated in macOS 10.11 - Use the URL resource property kCFURLIsPackageKey or NSURLIsPackageKey instead. [-Wdeprecated-declarations]
88:24.21  2980 |   *aResult = !!(info.flags & kLSItemInfoIsPackage);
88:24.21       |                              ^
88:24.21 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:43:3: note: 'kLSItemInfoIsPackage' has been explicitly marked deprecated here
88:24.21    43 |   kLSItemInfoIsPackage                          __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use the URL resource property kCFURLIsPackageKey or NSURLIsPackageKey instead.") = 0x00000002, /* Packaged directory*/
88:24.21       |   ^
88:24.58 27 warnings generated.
88:24.63 xpcom/string
88:32.33 xpcom/threads
88:33.29 23 warnings generated.
88:33.30 xpfe/appshell
88:33.34 js/xpconnect/shell
88:47.36 media/ffvpx/libavcodec/libmozavcodec.dylib.symbols.stub
88:48.25 media/ffvpx/libavcodec/bsf
88:49.69 media/ffvpx/libavcodec
88:49.74 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/allcodecs.c:31:
88:49.74 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components.h:22:
88:49.74 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
88:49.74    31 | #define CONFIG_NULL_BSF 0
88:49.74       |         ^
88:49.74 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: note: previous definition is here
88:49.74   673 | #define CONFIG_NULL_BSF 1
88:49.74       |         ^
88:49.83 1 warning generated.
88:50.32 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/av1dec.c:23:
88:50.32 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/hdr_dynamic_metadata.h:24:
88:50.32 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/frame.h:31:
88:50.32 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avutil.h:301:
88:50.32 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
88:50.32 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
88:50.32 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
88:50.32   673 | #define CONFIG_NULL_BSF 1
88:50.32       |         ^
88:50.32 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
88:50.32    31 | #define CONFIG_NULL_BSF 0
88:50.32       |         ^
88:51.11 1 warning generated.
88:51.66 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/bitstream_filters.c:72:
88:51.66 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/bsf_list.c:1:
88:51.66 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components.h:22:
88:51.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
88:51.67    31 | #define CONFIG_NULL_BSF 0
88:51.67       |         ^
88:51.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: note: previous definition is here
88:51.67   673 | #define CONFIG_NULL_BSF 1
88:51.67       |         ^
88:51.68 1 warning generated.
88:51.74 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/bsf.c:23:
88:51.74 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avassert.h:32:
88:51.74 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
88:51.74 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
88:51.75   673 | #define CONFIG_NULL_BSF 1
88:51.75       |         ^
88:51.75 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
88:51.75    31 | #define CONFIG_NULL_BSF 0
88:51.75       |         ^
88:51.89 1 warning generated.
88:57.23 media/ffvpx/libavcodec/x86
88:57.65 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/x86/idctdsp_init.c:29:22: warning: unused variable 'simple_mmx_permutation' [-Wunused-const-variable]
88:57.65    29 | static const uint8_t simple_mmx_permutation[64] = {
88:57.65       |                      ^~~~~~~~~~~~~~~~~~~~~~
88:57.67 1 warning generated.
89:05.06 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/idctdsp.c:20:
89:05.06 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components.h:22:
89:05.06 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:05.06    31 | #define CONFIG_NULL_BSF 0
89:05.06       |         ^
89:05.06 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: note: previous definition is here
89:05.06   673 | #define CONFIG_NULL_BSF 1
89:05.06       |         ^
89:05.25 1 warning generated.
89:06.22 media/ffvpx/libavutil/libmozavutil.dylib.symbols.stub
89:06.33 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/libaomenc.c:1450:36: warning: implicit conversion from enumeration type 'enum aom_com_control_id' to different enumeration type 'enum aome_enc_control_id' [-Wenum-conversion]
89:06.33  1450 |         res = codecctl_imgp(avctx, AV1_GET_NEW_FRAME_IMAGE, &img);
89:06.33       |               ~~~~~~~~~~~~~        ^~~~~~~~~~~~~~~~~~~~~~~
89:06.60 1 warning generated.
89:07.27 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/libvpxdec.c:33:
89:07.28 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
89:07.28 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
89:07.28 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:07.28   673 | #define CONFIG_NULL_BSF 1
89:07.28       |         ^
89:07.28 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
89:07.28    31 | #define CONFIG_NULL_BSF 0
89:07.28       |         ^
89:07.36 1 warning generated.
89:07.43 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/libvpxenc.c:33:
89:07.43 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/avcodec.h:32:
89:07.43 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avutil.h:301:
89:07.43 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
89:07.43 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
89:07.43 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:07.43   673 | #define CONFIG_NULL_BSF 1
89:07.43       |         ^
89:07.43 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
89:07.43    31 | #define CONFIG_NULL_BSF 0
89:07.43       |         ^
89:07.85 media/ffvpx/libavutil/x86
89:07.89 1 warning generated.
89:08.29 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/mpegaudiodec_fixed.c:22:
89:08.29 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components.h:22:
89:08.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:08.29    31 | #define CONFIG_NULL_BSF 0
89:08.29       |         ^
89:08.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: note: previous definition is here
89:08.29   673 | #define CONFIG_NULL_BSF 1
89:08.29       |         ^
89:09.67 1 warning generated.
89:09.77 dom/media/eme/clearkey
89:10.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/options.c:29:
89:10.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/avcodec.h:32:
89:10.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avutil.h:301:
89:10.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
89:10.35 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
89:10.35 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:10.35   673 | #define CONFIG_NULL_BSF 1
89:10.35       |         ^
89:10.35 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
89:10.35    31 | #define CONFIG_NULL_BSF 0
89:10.35       |         ^
89:10.39 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/options.c:39:
89:10.39 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/options_table.h:50:110: warning: implicit conversion from 'long long' to 'double' changes value from 9223372036854775807 to 9223372036854775808 [-Wimplicit-const-int-float-conversion]
89:10.39    50 | {"b", "set bitrate (in bits/s)", OFFSET(bit_rate), AV_OPT_TYPE_INT64, {.i64 = AV_CODEC_DEFAULT_BITRATE }, 0, INT64_MAX, A|V|E},
89:10.39       | ~                                                                                                            ^~~~~~~~~
89:10.39 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdint.h:94:26: note: expanded from macro 'INT64_MAX'
89:10.39    94 | #define INT64_MAX        9223372036854775807LL
89:10.39       |                          ^~~~~~~~~~~~~~~~~~~~~
89:10.44 2 warnings generated.
89:10.97 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/parsers.c:84:
89:10.97 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/parser_list.c:1:
89:10.97 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components.h:22:
89:10.98 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:10.98    31 | #define CONFIG_NULL_BSF 0
89:10.98       |         ^
89:10.98 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: note: previous definition is here
89:10.98   673 | #define CONFIG_NULL_BSF 1
89:10.98       |         ^
89:10.99 1 warning generated.
89:11.03 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/pcm.c:28:
89:11.03 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components.h:22:
89:11.03 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:11.03    31 | #define CONFIG_NULL_BSF 0
89:11.03       |         ^
89:11.03 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: note: previous definition is here
89:11.03   673 | #define CONFIG_NULL_BSF 1
89:11.03       |         ^
89:11.29 1 warning generated.
89:13.98 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vorbis_parser.c:33:
89:13.98 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/get_bits.h:31:
89:13.98 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
89:13.98 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
89:13.98 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:13.98   673 | #define CONFIG_NULL_BSF 1
89:13.98       |         ^
89:13.98 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
89:13.98    31 | #define CONFIG_NULL_BSF 0
89:13.98       |         ^
89:14.10 1 warning generated.
89:14.14 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vp8.c:30:
89:14.14 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/mem_internal.h:24:
89:14.15 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
89:14.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:14.15   673 | #define CONFIG_NULL_BSF 1
89:14.15       |         ^
89:14.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
89:14.15    31 | #define CONFIG_NULL_BSF 0
89:14.15       |         ^
89:16.93 1 warning generated.
89:17.14 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vp8dsp.c:30:
89:17.15 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
89:17.15 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
89:17.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:17.15   673 | #define CONFIG_NULL_BSF 1
89:17.15       |         ^
89:17.15 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
89:17.15    31 | #define CONFIG_NULL_BSF 0
89:17.15       |         ^
89:18.27 1 warning generated.
89:18.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/vp9.c:26:
89:18.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/avcodec.h:32:
89:18.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/avutil.h:301:
89:18.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/common.h:47:
89:18.34 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config.h:50:
89:18.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_darwin64.h:673:9: warning: 'CONFIG_NULL_BSF' macro redefined [-Wmacro-redefined]
89:18.34   673 | #define CONFIG_NULL_BSF 1
89:18.34       |         ^
89:18.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/config_components_audio_video.h:31:9: note: previous definition is here
89:18.34    31 | #define CONFIG_NULL_BSF 0
89:18.34       |         ^
89:20.10 1 warning generated.
89:25.87 media/gmp-clearkey/0.1
89:35.21 modules/xz-embedded
89:36.37 security/manager/ssl/builtins/dynamic-library/libnssckbi.dylib.symbols.stub
89:36.63 security/manager/ssl/ipcclientcerts/dynamic-library/libipcclientcerts.dylib.symbols.stub
89:36.83 security/manager/ssl/osclientcerts/dynamic-library/libosclientcerts.dylib.symbols.stub
89:36.88 security/nss/cmd/certutil
89:37.70 security/nss/cmd/lib
89:38.20 security/nss/cmd/pk12util
89:38.61 security/nss/lib/ckfw
89:39.93 security/nss/lib/crmf
89:40.59 security/nss/lib/freebl/out.freebl.def.stub
89:40.94 security/nss/lib/freebl
89:42.97 security/nss/lib/jar
89:44.00 security/nss/lib/softoken/out.softokn.def.stub
89:44.66 security/nss/lib/softoken
89:45.46 toolkit/components/telemetry/pingsender
89:47.21 toolkit/mozapps/macos-frameworks/ChannelPrefs-localbuild
89:47.48 tools/power
89:48.25 build/pure_virtual/libpure_virtual.a
89:48.49 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/tools/power/rapl.cpp:628:5: warning: 'sprintf' is deprecated: This function is provided for compatibility reasons only.  Due to security concerns inherent in the design of sprintf(3), it is highly recommended that you use snprintf(3) instead. [-Wdeprecated-declarations]
89:48.49   628 |     sprintf(aBuf, "%s", " n/a ");
89:48.49       |     ^
89:48.49 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdio.h:180:1: note: 'sprintf' has been explicitly marked deprecated here
89:48.49   180 | __deprecated_msg("This function is provided for compatibility reasons only.  Due to security concerns inherent in the design of sprintf(3), it is highly recommended that you use snprintf(3) instead.")
89:48.49       | ^
89:48.49 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/sys/cdefs.h:218:48: note: expanded from macro '__deprecated_msg'
89:48.49   218 |         #define __deprecated_msg(_msg) __attribute__((__deprecated__(_msg)))
89:48.49       |                                                       ^
89:48.49 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/tools/power/rapl.cpp:630:5: warning: 'sprintf' is deprecated: This function is provided for compatibility reasons only.  Due to security concerns inherent in the design of sprintf(3), it is highly recommended that you use snprintf(3) instead. [-Wdeprecated-declarations]
89:48.49   630 |     sprintf(aBuf, "%5.2f", JoulesToWatts(aValue_J));
89:48.49       |     ^
89:48.49 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdio.h:180:1: note: 'sprintf' has been explicitly marked deprecated here
89:48.49   180 | __deprecated_msg("This function is provided for compatibility reasons only.  Due to security concerns inherent in the design of sprintf(3), it is highly recommended that you use snprintf(3) instead.")
89:48.49       | ^
89:48.49 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/sys/cdefs.h:218:48: note: expanded from macro '__deprecated_msg'
89:48.49   218 |         #define __deprecated_msg(_msg) __attribute__((__deprecated__(_msg)))
89:48.49       |                                                       ^
89:48.74 2 warnings generated.
89:48.79 dom/media/fake-cdm/libfake.dylib
89:48.96 dom/media/gmp-plugin-openh264/libfakeopenh264.dylib
89:49.11 accessible/mac
89:50.09 dom/base
89:52.20    Compiling serde_json v1.0.116
89:52.76    Compiling percent-encoding v2.3.1
89:53.34    Compiling form_urlencoded v1.2.1
89:53.68    Compiling idna v1.0.3
89:59.85    Compiling url v2.5.4
90:02.84    Compiling mozilla-central-workspace-hack v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/build/workspace-hack)
90:02.93    Compiling nmhproxy v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/browser/app/nmhproxy)
90:04.59 dom/origin-trials
90:05.38 warning: stripping debug info with `rust-objcopy` failed: exit status: 127
90:05.38   |
90:05.38   = note: rust-objcopy: error while loading shared libraries: libLLVM.so.21.1-rust-1.94.1-stable: cannot open shared object file: No such file or directory
90:05.39 warning: `nmhproxy` (bin "nmhproxy") generated 1 warning
90:05.39     Finished `release` profile [optimized] target(s) in 17.16s
90:06.04 browser/app/nmhproxy/nmhproxy
90:07.65 js/src/gc
90:43.40 layout/style
91:10.60 media/libdav1d
91:41.01 netwerk/base
91:43.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsURLHelperOSX.cpp:40:15: warning: 'FSGetVolumeInfo' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
91:43.90    40 |       err = ::FSGetVolumeInfo(0, volumeIndex, nullptr, kFSVolInfoNone, nullptr,
91:43.90       |               ^
91:43.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:3936:15: note: 'FSGetVolumeInfo' has been explicitly marked deprecated here
91:43.90  3936 | extern OSErr  FSGetVolumeInfo(FSVolumeRefNum volume, ItemCount volumeIndex, FSVolumeRefNum *actualVolume, FSVolumeInfoBitmap whichInfo, FSVolumeInfo *info, HFSUniStr255 *volumeName, FSRef *rootDirectory) __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
91:43.90       |               ^
91:43.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsURLHelperOSX.cpp:86:51: warning: 'kCFURLHFSPathStyle' is deprecated: first deprecated in macOS 10.9 - Carbon File Manager is deprecated, use kCFURLPOSIXPathStyle where possible [-Wdeprecated-declarations]
91:43.90    86 |                                                   kCFURLHFSPathStyle, true);
91:43.90       |                                                   ^
91:43.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreFoundation.framework/Headers/CFURL.h:23:5: note: 'kCFURLHFSPathStyle' has been explicitly marked deprecated here
91:43.90    23 |     kCFURLHFSPathStyle API_DEPRECATED("Carbon File Manager is deprecated, use kCFURLPOSIXPathStyle where possible", macos(10.0,10.9), ios(2.0,7.0), watchos(2.0,2.0), tvos(9.0,9.0)), /* The use of kCFURLHFSPathStyle is deprecated. The Carbon File Manager, which uses HFS style paths, is deprecated. HFS style paths are unreliable because they can arbitrarily refer to multiple volumes if those volumes have identical volume names. You should instead use kCFURLPOSIXPathStyle wherever possible. */
91:43.90       |     ^
91:43.92 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsURLHelperOSX.cpp:167:13: warning: 'FSPathMakeRef' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
91:43.93   167 |       if (::FSPathMakeRef((UInt8*)possibleVolName.get(), &testRef, nullptr) !=
91:43.93       |             ^
91:43.93 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:4115:18: note: 'FSPathMakeRef' has been explicitly marked deprecated here
91:43.93  4115 | extern OSStatus  FSPathMakeRef(const UInt8 *path, FSRef *ref, Boolean *isDirectory)        __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
91:43.93       |                  ^
91:44.55 3 warnings generated.
92:06.32 netwerk/dns
93:38.87 security/manager/ssl
93:43.21 toolkit/components/telemetry
93:55.23 toolkit/library/buildid.cpp.stub
93:55.46 toolkit/library
94:14.37 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
94:14.37 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
94:14.37 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:91:11: error: redefinition of 'end' with a different type: 'char *' vs 'size_t' (aka 'unsigned long')
94:14.37    91 |     char* end = nullptr;
94:14.37       |           ^
94:14.37 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:83:12: note: previous definition is here
94:14.37    83 |     size_t end = token.find_last_not_of(" \t");
94:14.37       |            ^
94:14.37 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:92:53: error: cannot initialize a parameter of type 'char **' with an rvalue of type 'size_t *' (aka 'unsigned long *')
94:14.37    92 |     unsigned long val = std::strtoul(token.c_str(), &end, 16);
94:14.37       |                                                     ^~~~
94:14.37 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdlib.h:175:37: note: passing argument to parameter '__endptr' here
94:14.37   175 |          strtoul(const char *__str, char **__endptr, int __base);
94:14.37       |                                            ^
94:14.37 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
94:14.37 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
94:14.37 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:27: error: comparison between pointer and integer ('size_t' (aka 'unsigned long') and 'const value_type *' (aka 'const char *'))
94:14.37    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
94:14.37       |                       ~~~ ^  ~~~~~~~~~~~~~
94:14.37 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:47: error: indirection requires pointer operand ('size_t' (aka 'unsigned long') invalid)
94:14.37    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
94:14.37       |                                               ^~~~
94:25.70 4 errors generated.
94:25.77 gmake[5]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:674: Unified_cpp_security_manager_ssl2.o] Error 1
94:25.77 gmake[4]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:72: security/manager/ssl/target-objects] Error 2
94:25.77 gmake[4]: *** Waiting for unfinished jobs....
96:04.33 gmake[3]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:34: compile] Error 2
96:04.37 gmake[2]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:359: default] Error 2
96:04.40 gmake[1]: *** [client.mk:60: build] Error 2
96:04.51 W 1005 compiler warnings present.
96:06.28 W Notification center failed: Install notify-send (usually part of the libnotify package) to get a notification when the build finishes.
 Config object not found by mach.
Configure complete!
Be sure to run |mach build| to pick up any changes
  Parallelism determined by memory: using 4 jobs for 4 cores based on 15.6 GiB RAM and estimated job size of 1.0 GiB
make: *** [Makefile:132: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.

build (macos, arm64, ubuntu-24.04)

81:39.10 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/toolkit/xre/MacLaunchHelper.mm:190:53: warning: 'NSSocketPortNameServer' is deprecated: first deprecated in macOS 10.13 - Use NSXPCConnection instead [-Wdeprecated-declarations]
81:39.10   190 |                                    usingNameServer:[NSSocketPortNameServer
81:39.10       |                                                     ^
81:39.10 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSPortNameServer.h:78:12: note: 'NSSocketPortNameServer' has been explicitly marked deprecated here
81:39.10    78 | @interface NSSocketPortNameServer : NSPortNameServer
81:39.10       |            ^
81:40.02 view
81:44.14 2 warnings generated.
81:44.19 widget/cocoa
82:08.01 widget/headless
82:11.39 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsChildView.mm:69:
82:11.39 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-aarch64-apple-darwin/dist/include/GLContextCGL.h:32:3: warning: 'NSOpenGLContext' is deprecated: first deprecated in macOS 10.14 - Please use Metal or MetalKit. [-Wdeprecated-declarations]
82:11.39    32 |   NSOpenGLContext* mContext;
82:11.39       |   ^
82:11.39 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSOpenGL.h:184:12: note: 'NSOpenGLContext' has been explicitly marked deprecated here
82:11.40   184 | @interface NSOpenGLContext : NSObject <NSLocking>
82:11.40       |            ^
82:11.40 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsChildView.mm:69:
82:11.40 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-aarch64-apple-darwin/dist/include/GLContextCGL.h:38:38: warning: 'NSOpenGLContext' is deprecated: first deprecated in macOS 10.14 - Please use Metal or MetalKit. [-Wdeprecated-declarations]
82:11.40    38 |   GLContextCGL(const GLContextDesc&, NSOpenGLContext* context);
82:11.40       |                                      ^
82:11.40 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSOpenGL.h:184:12: note: 'NSOpenGLContext' has been explicitly marked deprecated here
82:11.40   184 | @interface NSOpenGLContext : NSObject <NSLocking>
82:11.40       |            ^
82:11.40 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsChildView.mm:69:
82:11.40 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/obj-aarch64-apple-darwin/dist/include/GLContextCGL.h:51:3: warning: 'NSOpenGLContext' is deprecated: first deprecated in macOS 10.14 - Please use Metal or MetalKit. [-Wdeprecated-declarations]
82:11.40    51 |   NSOpenGLContext* GetNSOpenGLContext() const { return mContext; }
82:11.40       |   ^
82:11.40 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSOpenGL.h:184:12: note: 'NSOpenGLContext' has been explicitly marked deprecated here
82:11.40   184 | @interface NSOpenGLContext : NSObject <NSLocking>
82:11.40       |            ^
82:14.48 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsChildView.mm:2065:51: warning: 'NSFilenamesPboardType' is deprecated: first deprecated in macOS 10.14 - Create multiple pasteboard items with NSPasteboardTypeFileURL or kUTTypeFileURL instead [-Wdeprecated-declarations]
82:14.48  2065 |                   [UTIHelper stringFromPboardType:NSFilenamesPboardType],
82:14.48       |                                                   ^
82:14.48 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSPasteboard.h:312:32: note: 'NSFilenamesPboardType' has been explicitly marked deprecated here
82:14.48   312 | APPKIT_EXTERN NSPasteboardType NSFilenamesPboardType API_DEPRECATED("Create multiple pasteboard items with NSPasteboardTypeFileURL or kUTTypeFileURL instead", macos(10.0,10.14));
82:14.48       |                                ^
82:14.55 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsChildView.mm:4549:58: warning: 'NSStringPboardType' is deprecated: first deprecated in macOS 10.14 [-Wdeprecated-declarations]
82:14.55  4549 |           containsObject:[UTIHelper stringFromPboardType:NSStringPboardType]] &&
82:14.55       |                                                          ^~~~~~~~~~~~~~~~~~
82:14.55       |                                                          NSPasteboardTypeString
82:14.55 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSPasteboard.h:311:32: note: 'NSStringPboardType' has been explicitly marked deprecated here
82:14.55   311 | APPKIT_EXTERN NSPasteboardType NSStringPboardType API_DEPRECATED_WITH_REPLACEMENT("NSPasteboardTypeString", macos(10.0,10.14));
82:14.55       |                                ^
82:15.40 widget
82:23.29 5 warnings generated.
82:23.38 xpcom/base
82:34.29 In file included from Unified_mm_widget_cocoa0.mm:56:
82:34.29 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.mm:6:
82:34.29 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.h:41:19: warning: 'NSUserNotificationActivationType' is deprecated: first deprecated in macOS 11.0 - All NSUserNotifications API should be replaced with UserNotifications.frameworks API [-Wdeprecated-declarations]
82:34.29    41 |                   NSUserNotificationActivationType aActivationType,
82:34.29       |                   ^
82:34.29 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSUserNotification.h:15:28: note: 'NSUserNotificationActivationType' has been explicitly marked deprecated here
82:34.29    15 | typedef NS_ENUM(NSInteger, NSUserNotificationActivationType) {
82:34.29       |                            ^
82:34.30 In file included from Unified_mm_widget_cocoa0.mm:56:
82:34.30 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.mm:39:21: warning: 'NSUserNotificationActivationType' is deprecated: first deprecated in macOS 11.0 - All NSUserNotifications API should be replaced with UserNotifications.frameworks API [-Wdeprecated-declarations]
82:34.30    39 | @property(readonly) NSUserNotificationActivationType activationType;
82:34.30       |                     ^
82:34.30 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSUserNotification.h:15:28: note: 'NSUserNotificationActivationType' has been explicitly marked deprecated here
82:34.30    15 | typedef NS_ENUM(NSInteger, NSUserNotificationActivationType) {
82:34.30       |                            ^
82:34.32 In file included from Unified_mm_widget_cocoa0.mm:56:
82:34.32 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.mm:274:45: warning: 'NSUserNotificationDefaultSoundName' is deprecated: first deprecated in macOS 11.0 - All NSUserNotifications API should be replaced with UserNotifications.frameworks API [-Wdeprecated-declarations]
82:34.32   274 |   notification.soundName = isSilent ? nil : NSUserNotificationDefaultSoundName;
82:34.32       |                                             ^
82:34.32 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSUserNotification.h:115:36: note: 'NSUserNotificationDefaultSoundName' has been explicitly marked deprecated here
82:34.32   115 | FOUNDATION_EXPORT NSString * const NSUserNotificationDefaultSoundName API_DEPRECATED("All NSUserNotifications API should be replaced with UserNotifications.frameworks API", macos(10.8, 11.0)) API_UNAVAILABLE(ios, watchos, tvos);
82:34.32       |                                    ^
82:34.34 In file included from Unified_mm_widget_cocoa0.mm:56:
82:34.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.mm:433:27: warning: 'NSUserNotificationActivationType' is deprecated: first deprecated in macOS 11.0 - All NSUserNotifications API should be replaced with UserNotifications.frameworks API [-Wdeprecated-declarations]
82:34.34   433 |     NSString* aAlertName, NSUserNotificationActivationType aActivationType,
82:34.34       |                           ^
82:34.34 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSUserNotification.h:15:28: note: 'NSUserNotificationActivationType' has been explicitly marked deprecated here
82:34.34    15 | typedef NS_ENUM(NSInteger, NSUserNotificationActivationType) {
82:34.34       |                            ^
82:34.34 In file included from Unified_mm_widget_cocoa0.mm:56:
82:34.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.mm:446:16: warning: 'NSUserNotificationActivationTypeAdditionalActionClicked' is deprecated: first deprecated in macOS 11.0 - All NSUserNotifications API should be replaced with UserNotifications.frameworks API [-Wdeprecated-declarations]
82:34.34   446 |           case NSUserNotificationActivationTypeAdditionalActionClicked:
82:34.34       |                ^
82:34.34 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSUserNotification.h:15:28: note: 'NSUserNotificationActivationType' has been explicitly marked deprecated here
82:34.34    15 | typedef NS_ENUM(NSInteger, NSUserNotificationActivationType) {
82:34.34       |                            ^
82:34.34 In file included from Unified_mm_widget_cocoa0.mm:56:
82:34.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.mm:447:16: warning: 'NSUserNotificationActivationTypeActionButtonClicked' is deprecated: first deprecated in macOS 11.0 - All NSUserNotifications API should be replaced with UserNotifications.frameworks API [-Wdeprecated-declarations]
82:34.34   447 |           case NSUserNotificationActivationTypeActionButtonClicked:
82:34.34       |                ^
82:34.34 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSUserNotification.h:15:28: note: 'NSUserNotificationActivationType' has been explicitly marked deprecated here
82:34.34    15 | typedef NS_ENUM(NSInteger, NSUserNotificationActivationType) {
82:34.34       |                            ^
82:36.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsNativeThemeCocoa.mm:72:16: warning: 'controlTint' is deprecated: first deprecated in macOS 11.0 - The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing. [-Wdeprecated-declarations]
82:36.27    72 |   return [self controlTint];
82:36.27       |                ^
82:36.27 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: property 'controlTint' is declared deprecated here
82:36.27   328 | @property NSControlTint controlTint API_DEPRECATED("The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing.", macos(10.0, 11.0));
82:36.27       |                         ^
82:36.27 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: 'controlTint' has been explicitly marked deprecated here
82:36.27 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsNativeThemeCocoa.mm:232:27: warning: 'controlTint' is deprecated: first deprecated in macOS 11.0 - The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing. [-Wdeprecated-declarations]
82:36.28   232 |   tdi.enableState = [self controlTint] == NSClearControlTint
82:36.28       |                           ^
82:36.28 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: property 'controlTint' is declared deprecated here
82:36.28   328 | @property NSControlTint controlTint API_DEPRECATED("The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing.", macos(10.0, 11.0));
82:36.28       |                         ^
82:36.28 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: 'controlTint' has been explicitly marked deprecated here
82:36.30 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsNativeThemeCocoa.mm:961:9: warning: 'setControlTint:' is deprecated: first deprecated in macOS 11.0 - The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing. [-Wdeprecated-declarations]
82:36.31   961 |   [cell setControlTint:(aParams.controlParams.insideActiveWindow
82:36.31       |         ^
82:36.31 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: property 'controlTint' is declared deprecated here
82:36.31   328 | @property NSControlTint controlTint API_DEPRECATED("The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing.", macos(10.0, 11.0));
82:36.31       |                         ^
82:36.31 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: 'setControlTint:' has been explicitly marked deprecated here
82:36.32 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsNativeThemeCocoa.mm:1436:11: warning: 'setControlTint:' is deprecated: first deprecated in macOS 11.0 - The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing. [-Wdeprecated-declarations]
82:36.33  1436 |     [cell setControlTint:[NSColor currentControlTint]];
82:36.33       |           ^
82:36.33 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: property 'controlTint' is declared deprecated here
82:36.33   328 | @property NSControlTint controlTint API_DEPRECATED("The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing.", macos(10.0, 11.0));
82:36.33       |                         ^
82:36.33 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: 'setControlTint:' has been explicitly marked deprecated here
82:36.33 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsNativeThemeCocoa.mm:1438:11: warning: 'setControlTint:' is deprecated: first deprecated in macOS 11.0 - The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing. [-Wdeprecated-declarations]
82:36.33  1438 |     [cell setControlTint:NSClearControlTint];
82:36.33       |           ^
82:36.33 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: property 'controlTint' is declared deprecated here
82:36.33   328 | @property NSControlTint controlTint API_DEPRECATED("The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing.", macos(10.0, 11.0));
82:36.33       |                         ^
82:36.33 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: 'setControlTint:' has been explicitly marked deprecated here
82:36.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsNativeThemeCocoa.mm:1646:7: warning: 'setControlTint:' is deprecated: first deprecated in macOS 11.0 - The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing. [-Wdeprecated-declarations]
82:36.34  1646 |       setControlTint:(aParams.insideActiveWindow ? [NSColor currentControlTint]
82:36.34       |       ^
82:36.34 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: property 'controlTint' is declared deprecated here
82:36.34   328 | @property NSControlTint controlTint API_DEPRECATED("The controlTint property is not respected on 10.14 and later. For custom cells, use +[NSColor controlAccentColor] to respect the user's preferred accent color when drawing.", macos(10.0, 11.0));
82:36.34       |                         ^
82:36.34 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:328:25: note: 'setControlTint:' has been explicitly marked deprecated here
82:40.66 6 warnings generated.
82:40.74 xpcom/build/Services.cpp.stub
82:42.39 In file included from Unified_mm_widget_cocoa0.mm:137:
82:42.40 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaUtils.mm:97:30: warning: 'NSStringPboardType' is deprecated: first deprecated in macOS 10.14 [-Wdeprecated-declarations]
82:42.40    97 |       [aType isEqualToString:NSStringPboardType] ||
82:42.40       |                              ^~~~~~~~~~~~~~~~~~
82:42.40       |                              NSPasteboardTypeString
82:42.40 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSPasteboard.h:311:32: note: 'NSStringPboardType' has been explicitly marked deprecated here
82:42.40   311 | APPKIT_EXTERN NSPasteboardType NSStringPboardType API_DEPRECATED_WITH_REPLACEMENT("NSPasteboardTypeString", macos(10.0,10.14));
82:42.40       |                                ^
82:42.41 In file included from Unified_mm_widget_cocoa0.mm:137:
82:42.41 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaUtils.mm:286:9: warning: 'GetProcessInformation' is deprecated: first deprecated in macOS 10.9 [-Wdeprecated-declarations]
82:42.41   286 |   if (::GetProcessInformation(&processSerialNumber, &processInfoRec) == noErr) {
82:42.41       |         ^
82:42.41 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/ApplicationServices.framework/Frameworks/HIServices.framework/Headers/Processes.h:430:1: note: 'GetProcessInformation' has been explicitly marked deprecated here
82:42.41   430 | GetProcessInformation(
82:42.41       | ^
82:42.41 In file included from Unified_mm_widget_cocoa0.mm:137:
82:42.41 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaUtils.mm:289:11: warning: 'GetProcessInformation' is deprecated: first deprecated in macOS 10.9 [-Wdeprecated-declarations]
82:42.41   289 |     if (::GetProcessInformation(&processInfoRec.processLauncher,
82:42.41       |           ^
82:42.41 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/ApplicationServices.framework/Frameworks/HIServices.framework/Headers/Processes.h:430:1: note: 'GetProcessInformation' has been explicitly marked deprecated here
82:42.41   430 | GetProcessInformation(
82:42.41       | ^
82:53.84 9 warnings generated.
83:08.34 In file included from Unified_mm_widget_cocoa1.mm:2:
83:08.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaWindow.mm:1576:11: warning: 'NSDisableScreenUpdates' is deprecated: first deprecated in macOS 10.11 - As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSDisableScreenUpdates. [-Wdeprecated-declarations]
83:08.34  1576 |           NSDisableScreenUpdates();
83:08.34       |           ^
83:08.34 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h:235:20: note: 'NSDisableScreenUpdates' has been explicitly marked deprecated here
83:08.34   235 | APPKIT_EXTERN void NSDisableScreenUpdates(void) API_DEPRECATED("As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSDisableScreenUpdates.", macos(10.0,10.11));
83:08.34       |                    ^
83:08.34 In file included from Unified_mm_widget_cocoa1.mm:2:
83:08.34 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaWindow.mm:1584:11: warning: 'NSEnableScreenUpdates' is deprecated: first deprecated in macOS 10.11 - As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSEnableScreenUpdates. [-Wdeprecated-declarations]
83:08.34  1584 |           NSEnableScreenUpdates();
83:08.34       |           ^
83:08.34 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h:237:20: note: 'NSEnableScreenUpdates' has been explicitly marked deprecated here
83:08.34   237 | APPKIT_EXTERN void NSEnableScreenUpdates(void) API_DEPRECATED("As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSEnableScreenUpdates.", macos(10.0,10.11));
83:08.34       |                    ^
83:08.34 In file included from Unified_mm_widget_cocoa1.mm:2:
83:08.35 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaWindow.mm:1608:13: warning: 'NSDisableScreenUpdates' is deprecated: first deprecated in macOS 10.11 - As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSDisableScreenUpdates. [-Wdeprecated-declarations]
83:08.35  1608 |             NSDisableScreenUpdates();
83:08.35       |             ^
83:08.35 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h:235:20: note: 'NSDisableScreenUpdates' has been explicitly marked deprecated here
83:08.35   235 | APPKIT_EXTERN void NSDisableScreenUpdates(void) API_DEPRECATED("As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSDisableScreenUpdates.", macos(10.0,10.11));
83:08.35       |                    ^
83:08.35 In file included from Unified_mm_widget_cocoa1.mm:2:
83:08.35 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsCocoaWindow.mm:1616:13: warning: 'NSEnableScreenUpdates' is deprecated: first deprecated in macOS 10.11 - As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSEnableScreenUpdates. [-Wdeprecated-declarations]
83:08.35  1616 |             NSEnableScreenUpdates();
83:08.35       |             ^
83:08.35 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSGraphics.h:237:20: note: 'NSEnableScreenUpdates' has been explicitly marked deprecated here
83:08.35   237 | APPKIT_EXTERN void NSEnableScreenUpdates(void) API_DEPRECATED("As of 10.11 it is not generally necessary to take explicit action to achieve visual atomicity. +[NSAnimationContext runAnimationGroup:] and other similar methods can be used when a stronger than normal need for visual atomicity is required. The NSAnimationContext methods do not suffer from the same performance problems as NSEnableScreenUpdates.", macos(10.0,10.11));
83:08.35       |                    ^
83:10.85 In file included from Unified_mm_widget_cocoa1.mm:47:
83:10.85 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsLookAndFeel.mm:149:39: warning: 'secondarySelectedControlColor' is deprecated: first deprecated in macOS 11.0 [-Wdeprecated-declarations]
83:10.85   149 |           GetColorFromNSColor(NSColor.secondarySelectedControlColor), aScheme);
83:10.85       |                                       ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
83:10.85       |                                       unemphasizedSelectedContentBackgroundColor
83:10.85 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:415:46: note: property 'secondarySelectedControlColor' is declared deprecated here
83:10.85   415 | @property (class, strong, readonly) NSColor *secondarySelectedControlColor API_DEPRECATED_WITH_REPLACEMENT("unemphasizedSelectedContentBackgroundColor", macos(10.1, 11.0));
83:10.85       |                                              ^
83:10.85 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:415:46: note: 'secondarySelectedControlColor' has been explicitly marked deprecated here
83:10.85 In file included from Unified_mm_widget_cocoa1.mm:47:
83:10.85 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsLookAndFeel.mm:247:44: warning: 'scrollBarColor' is deprecated: first deprecated in macOS 11.0 - Use NSScroller instead [-Wdeprecated-declarations]
83:10.85   247 |       aColor = GetColorFromNSColor(NSColor.scrollBarColor);
83:10.85       |                                            ^
83:10.85 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:401:46: note: property 'scrollBarColor' is declared deprecated here
83:10.85   401 | @property (class, strong, readonly) NSColor *scrollBarColor API_DEPRECATED("Use NSScroller instead", macos(10.0, 11.0));
83:10.85       |                                              ^
83:10.85 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:401:46: note: 'scrollBarColor' has been explicitly marked deprecated here
83:10.85 In file included from Unified_mm_widget_cocoa1.mm:47:
83:10.85 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsLookAndFeel.mm:278:44: warning: 'windowFrameColor' is deprecated: first deprecated in macOS 11.0 - Use NSVisualEffectMaterialTitlebar [-Wdeprecated-declarations]
83:10.85   278 |       aColor = GetColorFromNSColor(NSColor.windowFrameColor);
83:10.85       |                                            ^
83:10.85 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:408:46: note: property 'windowFrameColor' is declared deprecated here
83:10.85   408 | @property (class, strong, readonly) NSColor *windowFrameColor API_DEPRECATED("Use NSVisualEffectMaterialTitlebar", macos(10.0, 11.0));
83:10.85       |                                              ^
83:10.85 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:408:46: note: 'windowFrameColor' has been explicitly marked deprecated here
83:10.85 In file included from Unified_mm_widget_cocoa1.mm:47:
83:10.85 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsLookAndFeel.mm:310:44: warning: 'secondarySelectedControlColor' is deprecated: first deprecated in macOS 11.0 [-Wdeprecated-declarations]
83:10.85   310 |       aColor = GetColorFromNSColor(NSColor.secondarySelectedControlColor);
83:10.85       |                                            ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
83:10.85       |                                            unemphasizedSelectedContentBackgroundColor
83:10.85 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:415:46: note: property 'secondarySelectedControlColor' is declared deprecated here
83:10.86   415 | @property (class, strong, readonly) NSColor *secondarySelectedControlColor API_DEPRECATED_WITH_REPLACEMENT("unemphasizedSelectedContentBackgroundColor", macos(10.1, 11.0));
83:10.86       |                                              ^
83:10.86 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:415:46: note: 'secondarySelectedControlColor' has been explicitly marked deprecated here
83:10.86 In file included from Unified_mm_widget_cocoa1.mm:47:
83:10.86 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsLookAndFeel.mm:326:39: warning: 'controlAlternatingRowBackgroundColors' is deprecated: first deprecated in macOS 11.0 [-Wdeprecated-declarations]
83:10.86   326 |           GetColorFromNSColor(NSColor.controlAlternatingRowBackgroundColors[0]);
83:10.86       |                                       ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
83:10.86       |                                       alternatingContentBackgroundColors
83:10.86 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:419:57: note: property 'controlAlternatingRowBackgroundColors' is declared deprecated here
83:10.86   419 | @property (class, strong, readonly) NSArray<NSColor *> *controlAlternatingRowBackgroundColors API_DEPRECATED_WITH_REPLACEMENT("alternatingContentBackgroundColors", macos(10.3, 11.0));
83:10.86       |                                                         ^
83:10.86 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:419:57: note: 'controlAlternatingRowBackgroundColors' has been explicitly marked deprecated here
83:10.86 In file included from Unified_mm_widget_cocoa1.mm:47:
83:10.86 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsLookAndFeel.mm:331:39: warning: 'controlAlternatingRowBackgroundColors' is deprecated: first deprecated in macOS 11.0 [-Wdeprecated-declarations]
83:10.86   331 |           GetColorFromNSColor(NSColor.controlAlternatingRowBackgroundColors[1]);
83:10.86       |                                       ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
83:10.86       |                                       alternatingContentBackgroundColors
83:10.86 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:419:57: note: property 'controlAlternatingRowBackgroundColors' is declared deprecated here
83:10.86   419 | @property (class, strong, readonly) NSArray<NSColor *> *controlAlternatingRowBackgroundColors API_DEPRECATED_WITH_REPLACEMENT("alternatingContentBackgroundColors", macos(10.3, 11.0));
83:10.86       |                                                         ^
83:10.86 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSColor.h:419:57: note: 'controlAlternatingRowBackgroundColors' has been explicitly marked deprecated here
83:10.87 In file included from Unified_mm_widget_cocoa1.mm:47:
83:10.87 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsLookAndFeel.mm:609:19: warning: 'NSControlTintDidChangeNotification' is deprecated: first deprecated in macOS 11.0 - Changes to the accent color can be manually observed by implementing -viewDidChangeEffectiveAppearance in a NSView subclass, or by Key-Value Observing the -effectiveAppearance property on NSApplication. Views are automatically redisplayed when the accent color changes. [-Wdeprecated-declarations]
83:10.87   609 |              name:NSControlTintDidChangeNotification
83:10.87       |                   ^
83:10.87 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSCell.h:359:34: note: 'NSControlTintDidChangeNotification' has been explicitly marked deprecated here
83:10.88   359 | APPKIT_EXTERN NSNotificationName NSControlTintDidChangeNotification API_DEPRECATED("Changes to the accent color can be manually observed by implementing -viewDidChangeEffectiveAppearance in a NSView subclass, or by Key-Value Observing the -effectiveAppearance property on NSApplication. Views are automatically redisplayed when the accent color changes.", macos(10.0, 11.0));
83:10.88       |                                  ^
83:11.06 In file included from Unified_mm_widget_cocoa1.mm:83:
83:11.07 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsMacSharingService.mm:163:43: warning: 'NSWorkspaceLaunchAsync' is deprecated: first deprecated in macOS 11.0 - When using NSWorkspaceOpenConfiguration, all launches are asynchronous. [-Wdeprecated-declarations]
83:11.07   163 |                                   options:NSWorkspaceLaunchAsync
83:11.07       |                                           ^
83:11.07 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSWorkspace.h:351:5: note: 'NSWorkspaceLaunchAsync' has been explicitly marked deprecated here
83:11.07   351 |     NSWorkspaceLaunchAsync                    API_DEPRECATED("When using NSWorkspaceOpenConfiguration, all launches are asynchronous.", macos(10.3, 11.0)) = 0x00010000,
83:11.07       |     ^
83:11.07 In file included from Unified_mm_widget_cocoa1.mm:83:
83:11.07 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsMacSharingService.mm:161:34: warning: 'openURLs:withAppBundleIdentifier:options:additionalEventParamDescriptor:launchIdentifiers:' is deprecated: first deprecated in macOS 11.0 - Use -[NSWorkspace openURLs:withApplicationAtURL:configuration:completionHandler:] instead. [-Wdeprecated-declarations]
83:11.07   161 |   [[NSWorkspace sharedWorkspace] openURLs:@[ prefPaneURL ]
83:11.07       |                                  ^
83:11.07 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSWorkspace.h:406:1: note: 'openURLs:withAppBundleIdentifier:options:additionalEventParamDescriptor:launchIdentifiers:' has been explicitly marked deprecated here
83:11.07   406 | - (BOOL)openURLs:(NSArray<NSURL *> *)urls withAppBundleIdentifier:(nullable NSString *)bundleIdentifier options:(NSWorkspaceLaunchOptions)options additionalEventParamDescriptor:(nullable NSAppleEventDescriptor *)descriptor launchIdentifiers:(NSArray<NSNumber *> * _Nullable * _Nullable)identifiers API_DEPRECATED("Use -[NSWorkspace openURLs:withApplicationAtURL:configuration:completionHandler:] instead.", macos(10.10, 11.0));
83:11.07       | ^
83:11.07 In file included from Unified_mm_widget_cocoa1.mm:83:
83:11.07 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsMacSharingService.mm:208:46: warning: 'NSSharingServiceNamePostOnTwitter' is deprecated: first deprecated in macOS 10.14 - This service is no longer included with the system. [-Wdeprecated-declarations]
83:11.07   208 |   NSArray* toShare = [[service name] isEqual:NSSharingServiceNamePostOnTwitter]
83:11.07       |                                              ^
83:11.07 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSSharingService.h:39:42: note: 'NSSharingServiceNamePostOnTwitter' has been explicitly marked deprecated here
83:11.07    39 | APPKIT_EXTERN NSSharingServiceName const NSSharingServiceNamePostOnTwitter API_DEPRECATED("This service is no longer included with the system.", macos(10.8,10.14));
83:11.07       |                                          ^
83:11.09 In file included from Unified_mm_widget_cocoa1.mm:101:
83:11.09 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsMacWebAppUtils.mm:33:7: warning: 'absolutePathForAppBundleWithIdentifier:' is deprecated: first deprecated in macOS 11.0 - Use -[NSWorkspace URLForApplicationWithBundleIdentifier:] instead. [-Wdeprecated-declarations]
83:11.09    33 |       absolutePathForAppBundleWithIdentifier:
83:11.09       |       ^
83:11.09 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSWorkspace.h:400:1: note: 'absolutePathForAppBundleWithIdentifier:' has been explicitly marked deprecated here
83:11.09   400 | - (nullable NSString *)absolutePathForAppBundleWithIdentifier:(NSString *)bundleIdentifier API_DEPRECATED("Use -[NSWorkspace URLForApplicationWithBundleIdentifier:] instead.", macos(10.0, 11.0));
83:11.09       | ^
83:11.09 In file included from Unified_mm_widget_cocoa1.mm:101:
83:11.09 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsMacWebAppUtils.mm:58:8: warning: 'launchAppWithBundleIdentifier:options:additionalEventParamDescriptor:launchIdentifier:' is deprecated: first deprecated in macOS 11.0 - Use -[NSWorkspace openApplicationAtURL:configuration:completionHandler:] instead. [-Wdeprecated-declarations]
83:11.09    58 |        launchAppWithBundleIdentifier:
83:11.09       |        ^
83:11.09 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSWorkspace.h:405:1: note: 'launchAppWithBundleIdentifier:options:additionalEventParamDescriptor:launchIdentifier:' has been explicitly marked deprecated here
83:11.09   405 | - (BOOL)launchAppWithBundleIdentifier:(NSString *)bundleIdentifier options:(NSWorkspaceLaunchOptions)options additionalEventParamDescriptor:(nullable NSAppleEventDescriptor *)descriptor launchIdentifier:(NSNumber * _Nullable * _Nullable)identifier API_DEPRECATED("Use -[NSWorkspace openApplicationAtURL:configuration:completionHandler:] instead.", macos(10.0, 11.0));
83:11.09       | ^
83:11.40 In file included from Unified_mm_widget_cocoa2.mm:65:
83:11.40 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsSystemStatusBarCocoa.mm:48:15: warning: 'highlightMode' is deprecated: first deprecated in macOS 10.14 - Use the receiver's button.cell.highlightsBy instead [-Wdeprecated-declarations]
83:11.40    48 |   mStatusItem.highlightMode = YES;
83:11.40       |               ^
83:11.40 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/AppKit.framework/Headers/NSStatusItem.h:78:16: note: 'highlightMode' has been explicitly marked deprecated here
83:11.40    78 | @property BOOL highlightMode API_DEPRECATED("Use the receiver's button.cell.highlightsBy instead", macos(10.0,10.14));
83:11.40       |                ^
83:14.52 In file included from Unified_mm_widget_cocoa2.mm:128:
83:14.52 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/nsWidgetFactory.mm:33:
83:14.52 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/widget/cocoa/OSXNotificationCenter.h:41:19: warning: 'NSUserNotificationActivationType' is deprecated: first deprecated in macOS 11.0 - All NSUserNotifications API should be replaced with UserNotifications.frameworks API [-Wdeprecated-declarations]
83:14.52    41 |                   NSUserNotificationActivationType aActivationType,
83:14.52       |                   ^
83:14.52 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/Foundation.framework/Headers/NSUserNotification.h:15:28: note: 'NSUserNotificationActivationType' has been explicitly marked deprecated here
83:14.52    15 | typedef NS_ENUM(NSInteger, NSUserNotificationActivationType) {
83:14.52       |                            ^
83:19.81 16 warnings generated.
83:19.92 xpcom/components
83:20.75 2 warnings generated.
83:40.43 xpcom/ds
83:52.67 In file included from Unified_mm_xpcom_base0.mm:11:
83:52.67 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/base/MacStringHelpers.mm:24:11: warning: result of comparison 'NSUInteger' (aka 'unsigned long') > 18446744073709551615 is always false [-Wtautological-type-limit-compare]
83:52.67    24 |   if (len > std::numeric_limits<nsAString::size_type>::max()) {
83:52.67       |       ~~~ ^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
83:53.77 1 warning generated.
84:01.28 xpcom/io
84:09.89 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.89 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:483:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.89   483 |       return GetOSXFolderType(kUserDomain, kTemporaryFolderType, aFile);
84:09.89       |                               ^
84:09.89 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.89    63 | enum {
84:09.89       | ^
84:09.89 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.89 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:483:44: warning: 'kTemporaryFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.89   483 |       return GetOSXFolderType(kUserDomain, kTemporaryFolderType, aFile);
84:09.89       |                                            ^
84:09.89 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.89   302 | enum {
84:09.89       | ^
84:09.89 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.89 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:508:31: warning: 'kClassicDomain' is deprecated: first deprecated in macOS 10.5 - Deprecated [-Wdeprecated-declarations]
84:09.89   508 |       return GetOSXFolderType(kClassicDomain, kSystemFolderType, aFile);
84:09.89       |                               ^
84:09.89 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:75:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:75:1)' has been explicitly marked deprecated here
84:09.89    75 | enum {
84:09.89       | ^
84:09.89 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.89 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:508:47: warning: 'kSystemFolderType' is deprecated: first deprecated in macOS 10.5 - Deprecated [-Wdeprecated-declarations]
84:09.89   508 |       return GetOSXFolderType(kClassicDomain, kSystemFolderType, aFile);
84:09.89       |                                               ^
84:09.89 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:450:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:450:1)' has been explicitly marked deprecated here
84:09.89   450 | enum {
84:09.89       | ^
84:09.89 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.89 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:511:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.89   511 |       return GetOSXFolderType(kUserDomain, kDomainLibraryFolderType, aFile);
84:09.89       |                               ^
84:09.89 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.89    63 | enum {
84:09.89       | ^
84:09.89 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.89 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:511:44: warning: 'kDomainLibraryFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.89   511 |       return GetOSXFolderType(kUserDomain, kDomainLibraryFolderType, aFile);
84:09.89       |                                            ^
84:09.89 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.89   302 | enum {
84:09.89       | ^
84:09.89 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:514:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   514 |       return GetOSXFolderType(kUserDomain, kDomainTopLevelFolderType, aFile);
84:09.90       |                               ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:514:44: warning: 'kDomainTopLevelFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   514 |       return GetOSXFolderType(kUserDomain, kDomainTopLevelFolderType, aFile);
84:09.90       |                                            ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.90   302 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:517:38: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   517 |       nsresult rv = GetOSXFolderType(kUserDomain, kDownloadsFolderType, aFile);
84:09.90       |                                      ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:517:51: warning: 'kDownloadsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   517 |       nsresult rv = GetOSXFolderType(kUserDomain, kDownloadsFolderType, aFile);
84:09.90       |                                                   ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:371:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:371:1)' has been explicitly marked deprecated here
84:09.90   371 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:519:33: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   519 |         return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
84:09.90       |                                 ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:519:46: warning: 'kDesktopFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   519 |         return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
84:09.90       |                                              ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.90   302 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:524:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   524 |       return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
84:09.90       |                               ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:524:44: warning: 'kDesktopFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   524 |       return GetOSXFolderType(kUserDomain, kDesktopFolderType, aFile);
84:09.90       |                                            ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.90   302 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:527:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   527 |       return GetOSXFolderType(kUserDomain, kDocumentsFolderType, aFile);
84:09.90       |                               ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:527:44: warning: 'kDocumentsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   527 |       return GetOSXFolderType(kUserDomain, kDocumentsFolderType, aFile);
84:09.90       |                                            ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1)' has been explicitly marked deprecated here
84:09.90   341 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:530:31: warning: 'kLocalDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   530 |       return GetOSXFolderType(kLocalDomain, kApplicationsFolderType, aFile);
84:09.90       |                               ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:530:45: warning: 'kApplicationsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   530 |       return GetOSXFolderType(kLocalDomain, kApplicationsFolderType, aFile);
84:09.90       |                                             ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.90   302 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:533:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   533 |       return GetOSXFolderType(kUserDomain, kPreferencesFolderType, aFile);
84:09.90       |                               ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:533:44: warning: 'kPreferencesFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   533 |       return GetOSXFolderType(kUserDomain, kPreferencesFolderType, aFile);
84:09.90       |                                            ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.90   302 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:536:31: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   536 |       return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType, aFile);
84:09.90       |                               ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:536:44: warning: 'kPictureDocumentsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   536 |       return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType, aFile);
84:09.90       |                                            ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1)' has been explicitly marked deprecated here
84:09.90   341 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:544:33: warning: 'kUserDomain' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   544 |         return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType,
84:09.90       |                                 ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:63:1)' has been explicitly marked deprecated here
84:09.90    63 | enum {
84:09.90       | ^
84:09.90 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.90 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:544:46: warning: 'kPictureDocumentsFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.90   544 |         return GetOSXFolderType(kUserDomain, kPictureDocumentsFolderType,
84:09.90       |                                              ^
84:09.90 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:341:1)' has been explicitly marked deprecated here
84:09.90   341 | enum {
84:09.90       | ^
84:09.91 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.91 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:706:22: warning: 'kTemporaryFolderType' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.91   706 |   if (aFolderType == kTemporaryFolderType) {
84:09.91       |                      ^
84:09.91 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:302:1)' has been explicitly marked deprecated here
84:09.91   302 | enum {
84:09.91       | ^
84:09.91 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.91 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:716:11: warning: 'FSFindFolder' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
84:09.91   716 |   err = ::FSFindFolder(aDomain, aFolderType, kCreateFolder, &fsRef);
84:09.91       |           ^
84:09.91 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:289:1: note: 'FSFindFolder' has been explicitly marked deprecated here
84:09.91   289 | FSFindFolder(
84:09.91       | ^
84:09.91 In file included from Unified_cpp_xpcom_io0.cpp:101:
84:09.91 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/SpecialSystemDirectory.cpp:716:46: warning: 'kCreateFolder' is deprecated: first deprecated in macOS 10.8 - Deprecated [-Wdeprecated-declarations]
84:09.91   716 |   err = ::FSFindFolder(aDomain, aFolderType, kCreateFolder, &fsRef);
84:09.91       |                                              ^
84:09.91 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:87:1: note: '(unnamed enum at /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Folders.h:87:1)' has been explicitly marked deprecated here
84:09.91    87 | enum {
84:09.91       | ^
84:16.06 27 warnings generated.
84:21.38 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.38 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1994:36: warning: 'kLSRequestAllInfo' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
84:21.38  1994 |   LSRequestedInfo theInfoRequest = kLSRequestAllInfo;
84:21.38       |                                    ^
84:21.38 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:36:3: note: 'kLSRequestAllInfo' has been explicitly marked deprecated here
84:21.38    36 |   kLSRequestAllInfo                                     __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.") = (UInt32)0xFFFFFFFF /* thread-safe in 10.2*/
84:21.38       |   ^
84:21.38 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.38 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1995:3: warning: 'LSItemInfoRecord' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
84:21.38  1995 |   LSItemInfoRecord theInfo;
84:21.38       |   ^
84:21.38 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:67:3: note: 'LSItemInfoRecord' has been explicitly marked deprecated here
84:21.38    67 | } LSItemInfoRecord __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.");
84:21.38       |   ^
84:21.38 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.38 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1996:23: warning: 'LSCopyItemInfoForURL' is deprecated: first deprecated in macOS 10.11 - Use URL resource properties instead. [-Wdeprecated-declarations]
84:21.38  1996 |   OSStatus result = ::LSCopyItemInfoForURL(url, theInfoRequest, &theInfo);
84:21.38       |                       ^
84:21.38 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:103:1: note: 'LSCopyItemInfoForURL' has been explicitly marked deprecated here
84:21.38   103 | LSCopyItemInfoForURL(
84:21.38       | ^
84:21.38 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.38 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:1999:26: warning: 'kLSItemInfoIsApplication' is deprecated: first deprecated in macOS 10.11 - Use the URL resource property kCFURLIsApplicationKey or NSURLIsApplicationKey instead. [-Wdeprecated-declarations]
84:21.38  1999 |     if ((theInfo.flags & kLSItemInfoIsApplication) != 0) {
84:21.38       |                          ^
84:21.38 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:44:3: note: 'kLSItemInfoIsApplication' has been explicitly marked deprecated here
84:21.38    44 |   kLSItemInfoIsApplication                      __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use the URL resource property kCFURLIsApplicationKey or NSURLIsApplicationKey instead.") = 0x00000004, /* Single-file or packaged application*/
84:21.38       |   ^
84:21.41 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.41 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2325:25: warning: 'GetAliasSizeFromPtr' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
84:21.41  2325 |   int32_t aliasSize = ::GetAliasSizeFromPtr(&aliasHeader);
84:21.41       |                         ^
84:21.41 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Aliases.h:676:1: note: 'GetAliasSizeFromPtr' has been explicitly marked deprecated here
84:21.41   676 | GetAliasSizeFromPtr(const AliasRecord * alias)                __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_4, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
84:21.41       | ^
84:21.41 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.41 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2338:9: warning: 'PtrToHand' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
84:21.41  2338 |   if (::PtrToHand(decodedData, &newHandle, aliasSize) != noErr) {
84:21.41       |         ^
84:21.41 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/MacMemory.h:1773:1: note: 'PtrToHand' has been explicitly marked deprecated here
84:21.41  1773 | PtrToHand(
84:21.41       | ^
84:21.41 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.41 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2348:17: warning: 'FSResolveAlias' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
84:21.41  2348 |   OSErr err = ::FSResolveAlias(nullptr, (AliasHandle)newHandle, &resolvedFSRef,
84:21.41       |                 ^
84:21.41 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Aliases.h:260:1: note: 'FSResolveAlias' has been explicitly marked deprecated here
84:21.41   260 | FSResolveAlias(
84:21.41       | ^
84:21.42 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.42 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2352:3: warning: 'DisposeHandle' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
84:21.42  2352 |   DisposeHandle(newHandle);
84:21.42       |   ^
84:21.42 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/MacMemory.h:1279:1: note: 'DisposeHandle' has been explicitly marked deprecated here
84:21.42  1279 | DisposeHandle(Handle h)                                       __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
84:21.42       | ^
84:21.44 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.44 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2728:26: warning: 'CFURLCreateFromFSRef' is deprecated: first deprecated in macOS 10.9 - Not supported [-Wdeprecated-declarations]
84:21.44  2728 |   CFURLRef newURLRef = ::CFURLCreateFromFSRef(kCFAllocatorDefault, aFSRef);
84:21.44       |                          ^
84:21.44 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreFoundation.framework/Headers/CFURL.h:484:10: note: 'CFURLCreateFromFSRef' has been explicitly marked deprecated here
84:21.44   484 | CFURLRef CFURLCreateFromFSRef(CFAllocatorRef allocator, const struct FSRef *fsRef) API_DEPRECATED("Not supported", macos(10.0,10.9), ios(2.0,7.0), watchos(2.0,2.0), tvos(9.0,9.0));
84:21.44       |          ^
84:21.44 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.44 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2760:11: warning: 'CFURLGetFSRef' is deprecated: first deprecated in macOS 10.9 - Not supported [-Wdeprecated-declarations]
84:21.44  2760 |     if (::CFURLGetFSRef(url, aResult)) {
84:21.44       |           ^
84:21.44 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreFoundation.framework/Headers/CFURL.h:487:9: note: 'CFURLGetFSRef' has been explicitly marked deprecated here
84:21.44   487 | Boolean CFURLGetFSRef(CFURLRef url, struct FSRef *fsRef) API_DEPRECATED("Not supported", macos(10.0,10.9), ios(2.0,7.0), watchos(2.0,2.0), tvos(9.0,9.0));
84:21.44       |         ^
84:21.45 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.45 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2778:19: warning: 'FSGetCatalogInfo' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
84:21.45  2778 |     OSErr err = ::FSGetCatalogInfo(&fsRef, kFSCatInfoNone, nullptr, nullptr,
84:21.45       |                   ^
84:21.45 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:2620:15: note: 'FSGetCatalogInfo' has been explicitly marked deprecated here
84:21.45  2620 | extern OSErr  FSGetCatalogInfo(const FSRef *ref, FSCatalogInfoBitmap whichInfo, FSCatalogInfo *catalogInfo, HFSUniStr255 *outName, FSSpecPtr fsSpec, FSRef *parentRef) __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
84:21.45       |               ^
84:21.45 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.45 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2800:9: warning: 'FSGetCatalogInfo' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
84:21.45  2800 |       ::FSGetCatalogInfo(&fsRef, kFSCatInfoDataSizes + kFSCatInfoRsrcSizes,
84:21.45       |         ^
84:21.45 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:2620:15: note: 'FSGetCatalogInfo' has been explicitly marked deprecated here
84:21.45  2620 | extern OSErr  FSGetCatalogInfo(const FSRef *ref, FSCatalogInfoBitmap whichInfo, FSCatalogInfo *catalogInfo, HFSUniStr255 *outName, FSSpecPtr fsSpec, FSRef *parentRef) __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
84:21.45       |               ^
84:21.46 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2881:3: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
84:21.46  2881 |   LSLaunchFSRefSpec thelaunchSpec;
84:21.46       |   ^
84:21.46 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
84:21.46    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
84:21.46       |   ^
84:21.46 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2886:36: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
84:21.46  2886 |   memset(&thelaunchSpec, 0, sizeof(LSLaunchFSRefSpec));
84:21.46       |                                    ^
84:21.46 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
84:21.46    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
84:21.46       |   ^
84:21.46 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2895:17: warning: 'LSOpenFromRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSOpenFromURLSpec or NSWorkspace instead. [-Wdeprecated-declarations]
84:21.46  2895 |   OSErr err = ::LSOpenFromRefSpec(&thelaunchSpec, nullptr);
84:21.46       |                 ^
84:21.46 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:123:1: note: 'LSOpenFromRefSpec' has been explicitly marked deprecated here
84:21.46   123 | LSOpenFromRefSpec(
84:21.46       | ^
84:21.46 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.46 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2912:19: warning: 'LSOpenFSRef' is deprecated: first deprecated in macOS 10.10 - Use LSOpenCFURLRef or -[NSWorkspace openURL:] instead. [-Wdeprecated-declarations]
84:21.46  2912 |     OSErr err = ::LSOpenFSRef(&docFSRef, nullptr);
84:21.46       |                   ^
84:21.46 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:86:1: note: 'LSOpenFSRef' has been explicitly marked deprecated here
84:21.46    86 | LSOpenFSRef(
84:21.46       | ^
84:21.46 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.47 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2937:3: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
84:21.47  2937 |   LSLaunchFSRefSpec thelaunchSpec;
84:21.47       |   ^
84:21.47 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
84:21.47    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
84:21.47       |   ^
84:21.47 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.47 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2942:36: warning: 'LSLaunchFSRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSLaunchURLSpec instead. [-Wdeprecated-declarations]
84:21.47  2942 |   memset(&thelaunchSpec, 0, sizeof(LSLaunchFSRefSpec));
84:21.47       |                                    ^
84:21.47 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:47:3: note: 'LSLaunchFSRefSpec' has been explicitly marked deprecated here
84:21.47    47 | } LSLaunchFSRefSpec API_DEPRECATED("Use LSLaunchURLSpec instead.", macos(10.0,10.10) ) API_UNAVAILABLE( ios, tvos, watchos );
84:21.47       |   ^
84:21.47 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.47 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2949:17: warning: 'LSOpenFromRefSpec' is deprecated: first deprecated in macOS 10.10 - Use LSOpenFromURLSpec or NSWorkspace instead. [-Wdeprecated-declarations]
84:21.47  2949 |   OSErr err = ::LSOpenFromRefSpec(&thelaunchSpec, nullptr);
84:21.47       |                 ^
84:21.47 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSOpenDeprecated.h:123:1: note: 'LSOpenFromRefSpec' has been explicitly marked deprecated here
84:21.47   123 | LSOpenFromRefSpec(
84:21.47       | ^
84:21.47 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.47 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2970:3: warning: 'LSItemInfoRecord' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
84:21.47  2970 |   LSItemInfoRecord info;
84:21.47       |   ^
84:21.47 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:67:3: note: 'LSItemInfoRecord' has been explicitly marked deprecated here
84:21.47    67 | } LSItemInfoRecord __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.");
84:21.47       |   ^
84:21.47 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.47 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2972:9: warning: 'LSCopyItemInfoForURL' is deprecated: first deprecated in macOS 10.11 - Use URL resource properties instead. [-Wdeprecated-declarations]
84:21.47  2972 |       ::LSCopyItemInfoForURL(url, kLSRequestBasicFlagsOnly, &info);
84:21.47       |         ^
84:21.47 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:103:1: note: 'LSCopyItemInfoForURL' has been explicitly marked deprecated here
84:21.47   103 | LSCopyItemInfoForURL(
84:21.47       | ^
84:21.47 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.47 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2972:35: warning: 'kLSRequestBasicFlagsOnly' is deprecated: first deprecated in macOS 10.11 - Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead. [-Wdeprecated-declarations]
84:21.47  2972 |       ::LSCopyItemInfoForURL(url, kLSRequestBasicFlagsOnly, &info);
84:21.47       |                                   ^
84:21.47 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:31:3: note: 'kLSRequestBasicFlagsOnly' has been explicitly marked deprecated here
84:21.47    31 |   kLSRequestBasicFlagsOnly                      __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use CFURLCopyResourcePropertiesForKeys or -[NSURL resourceValuesForKeys:error:] instead.") = 0x00000004, /* thread-safe in 10.2*/
84:21.47       |   ^
84:21.47 In file included from Unified_cpp_xpcom_io1.cpp:47:
84:21.47 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/xpcom/io/nsLocalFileUnix.cpp:2980:30: warning: 'kLSItemInfoIsPackage' is deprecated: first deprecated in macOS 10.11 - Use the URL resource property kCFURLIsPackageKey or NSURLIsPackageKey instead. [-Wdeprecated-declarations]
84:21.47  2980 |   *aResult = !!(info.flags & kLSItemInfoIsPackage);
84:21.47       |                              ^
84:21.47 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Headers/LSInfoDeprecated.h:43:3: note: 'kLSItemInfoIsPackage' has been explicitly marked deprecated here
84:21.47    43 |   kLSItemInfoIsPackage                          __OS_AVAILABILITY_MSG(macosx, deprecated=10.11, "Use the URL resource property kCFURLIsPackageKey or NSURLIsPackageKey instead.") = 0x00000002, /* Packaged directory*/
84:21.47       |   ^
84:22.56 xpcom/reflect/xptcall/md/unix/xptcinvoke_asm_aarch64.o
84:22.56 xpcom/reflect/xptcall/md/unix/xptcstubs_asm_aarch64.o
84:22.69 xpcom/reflect/xptcall/md/unix
84:24.29 xpcom/reflect/xptcall
84:26.92 xpcom/reflect/xptinfo
84:30.51 23 warnings generated.
84:30.56 xpcom/string
84:32.84 xpcom/threads
84:35.54 xpfe/appshell
84:39.26 js/xpconnect/shell
84:42.52 media/ffvpx/libavcodec/libmozavcodec.dylib.symbols.stub
84:48.70 media/ffvpx/libavcodec/aarch64
84:49.62 media/ffvpx/libavcodec/aarch64/h264cmc_neon.o
84:49.83 media/ffvpx/libavcodec/aarch64/h264dsp_neon.o
84:49.91 media/ffvpx/libavcodec/aarch64/h264idct_neon.o
84:50.00 media/ffvpx/libavcodec/aarch64/h264pred_neon.o
84:50.08 media/ffvpx/libavcodec/aarch64/hpeldsp_neon.o
84:50.16 media/ffvpx/libavcodec/aarch64/idctdsp_neon.o
84:50.23 media/ffvpx/libavcodec/aarch64/mpegaudiodsp_neon.o
84:50.30 media/ffvpx/libavcodec/aarch64/neon.o
84:50.37 media/ffvpx/libavcodec/aarch64/simple_idct_neon.o
84:50.44 media/ffvpx/libavcodec/aarch64/videodsp.o
84:50.52 media/ffvpx/libavcodec/aarch64/vp8dsp_neon.o
84:50.58 media/ffvpx/libavcodec/aarch64/vp9itxfm_16bpp_neon.o
84:50.69 media/ffvpx/libavcodec/aarch64/vp9itxfm_neon.o
84:50.86 media/ffvpx/libavcodec/aarch64/vp9lpf_16bpp_neon.o
84:51.01 media/ffvpx/libavcodec/aarch64/vp9lpf_neon.o
84:51.09 media/ffvpx/libavcodec/aarch64/vp9mc_16bpp_neon.o
84:51.20 media/ffvpx/libavcodec/aarch64/vp9mc_aarch64.o
84:51.31 media/ffvpx/libavcodec/aarch64/vp9mc_neon.o
84:51.49 media/ffvpx/libavcodec/bsf
84:51.87 media/ffvpx/libavcodec
84:58.96 media/ffvpx/libavutil/libmozavutil.dylib.symbols.stub
84:59.36 media/ffvpx/libavutil/aarch64
84:59.45 media/ffvpx/libavutil/aarch64/float_dsp_neon.o
84:59.54 media/ffvpx/libavutil/aarch64/tx_float_neon.o
85:00.09 media/ffvpx/libavutil
85:02.23 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/cpu.c:72:12: warning: 'return' will never be executed [-Wunreachable-code-return]
85:02.23    72 |     return 0;
85:02.23       |            ^
85:02.23 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/cpu.c:116:76: warning: implicit conversion from 'long long' to 'double' changes value from 9223372036854775807 to 9223372036854775808 [-Wimplicit-const-int-float-conversion]
85:02.23   116 |         { "flags"   , NULL, 0, AV_OPT_TYPE_FLAGS, { .i64 = 0 }, INT64_MIN, INT64_MAX, .unit = "flags" },
85:02.23       |         ~                                                                  ^~~~~~~~~
85:02.23 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdint.h:94:26: note: expanded from macro 'INT64_MAX'
85:02.24    94 | #define INT64_MAX        9223372036854775807LL
85:02.24       |                          ^~~~~~~~~~~~~~~~~~~~~
85:02.24 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/cpu.c:284:12: warning: 'return' will never be executed [-Wunreachable-code-return]
85:02.24   284 |     return 8;
85:02.24       |            ^
85:02.25 3 warnings generated.
85:02.73 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/eval.c:249:29: warning: implicit conversion from 'unsigned long long' to 'double' changes value from 18446744073709551615 to 18446744073709551616 [-Wimplicit-const-int-float-conversion]
85:02.73   249 |             return r * (1.0/UINT64_MAX);
85:02.73       |                            ~^~~~~~~~~~
85:02.73 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdint.h:110:27: note: expanded from macro 'UINT64_MAX'
85:02.73   110 | #define UINT64_MAX        18446744073709551615ULL
85:02.73       |                           ^~~~~~~~~~~~~~~~~~~~~~~
85:02.73 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/eval.c:255:44: warning: implicit conversion from 'unsigned long long' to 'double' changes value from 18446744073709551615 to 18446744073709551616 [-Wimplicit-const-int-float-conversion]
85:02.73   255 |             return min + (max - min) * r / UINT64_MAX;
85:02.73       |                                          ~ ^~~~~~~~~~
85:02.73 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdint.h:110:27: note: expanded from macro 'UINT64_MAX'
85:02.73   110 | #define UINT64_MAX        18446744073709551615ULL
85:02.73       |                           ^~~~~~~~~~~~~~~~~~~~~~~
85:02.98 2 warnings generated.
85:06.08 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/opt.c:455:12: warning: 'return' will never be executed [-Wunreachable-code-return]
85:06.08   455 |     return 0;
85:06.08       |            ^
85:06.78 1 warning generated.
85:08.08 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/time.c:68:12: warning: 'return' will never be executed [-Wunreachable-code-return]
85:08.08    68 |     return av_gettime() + 42 * 60 * 60 * INT64_C(1000000);
85:08.08       |            ^~~~~~~~~~
85:08.08 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavutil/time.c:76:16: warning: 'return' will never be executed [-Wunreachable-code-return]
85:08.08    76 |         return 0;
85:08.08       |                ^
85:08.09 2 warnings generated.
85:10.47 dom/media/eme/clearkey
85:10.68 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/libaomenc.c:1450:36: warning: implicit conversion from enumeration type 'enum aom_com_control_id' to different enumeration type 'enum aome_enc_control_id' [-Wenum-conversion]
85:10.68  1450 |         res = codecctl_imgp(avctx, AV1_GET_NEW_FRAME_IMAGE, &img);
85:10.68       |               ~~~~~~~~~~~~~        ^~~~~~~~~~~~~~~~~~~~~~~
85:10.96 1 warning generated.
85:11.72 media/gmp-clearkey/0.1
85:12.76 modules/xz-embedded
85:13.51 security/manager/ssl/builtins/dynamic-library/libnssckbi.dylib.symbols.stub
85:13.76 security/manager/ssl/ipcclientcerts/dynamic-library/libipcclientcerts.dylib.symbols.stub
85:14.05 security/manager/ssl/osclientcerts/dynamic-library/libosclientcerts.dylib.symbols.stub
85:14.19 security/nss/cmd/certutil
85:14.45 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/options.c:39:
85:14.45 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/media/ffvpx/libavcodec/options_table.h:50:110: warning: implicit conversion from 'long long' to 'double' changes value from 9223372036854775807 to 9223372036854775808 [-Wimplicit-const-int-float-conversion]
85:14.45    50 | {"b", "set bitrate (in bits/s)", OFFSET(bit_rate), AV_OPT_TYPE_INT64, {.i64 = AV_CODEC_DEFAULT_BITRATE }, 0, INT64_MAX, A|V|E},
85:14.45       | ~                                                                                                            ^~~~~~~~~
85:14.45 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdint.h:94:26: note: expanded from macro 'INT64_MAX'
85:14.45    94 | #define INT64_MAX        9223372036854775807LL
85:14.45       |                          ^~~~~~~~~~~~~~~~~~~~~
85:14.50 1 warning generated.
85:14.96 security/nss/cmd/lib
85:15.29 security/nss/cmd/pk12util
85:15.83 security/nss/lib/ckfw
85:17.17 security/nss/lib/crmf
85:18.17 security/nss/lib/freebl/out.freebl.def.stub
85:18.56 security/nss/lib/freebl
85:19.80 security/nss/lib/jar
85:23.65 security/nss/lib/softoken/out.softokn.def.stub
85:25.01 security/nss/lib/softoken
85:31.72 toolkit/components/telemetry/pingsender
85:33.64 toolkit/mozapps/macos-frameworks/ChannelPrefs-localbuild
85:36.38 build/pure_virtual/libpure_virtual.a
85:36.70 dom/media/fake-cdm/libfake.dylib
85:36.89 dom/media/gmp-plugin-openh264/libfakeopenh264.dylib
85:38.67    Compiling percent-encoding v2.3.1
85:38.90    Compiling serde_json v1.0.116
85:39.13    Compiling form_urlencoded v1.2.1
85:39.27    Compiling idna v1.0.3
85:39.97 accessible/mac
85:42.13    Compiling url v2.5.4
85:42.34 dom/base
85:45.18    Compiling mozilla-central-workspace-hack v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/build/workspace-hack)
85:45.26    Compiling nmhproxy v0.1.0 (/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/browser/app/nmhproxy)
85:47.80 warning: stripping debug info with `rust-objcopy` failed: exit status: 127
85:47.80   |
85:47.80   = note: rust-objcopy: error while loading shared libraries: libLLVM.so.21.1-rust-1.94.1-stable: cannot open shared object file: No such file or directory
85:47.81 warning: `nmhproxy` (bin "nmhproxy") generated 1 warning
85:47.81     Finished `release` profile [optimized] target(s) in 12.65s
85:48.47 browser/app/nmhproxy/nmhproxy
85:59.54 dom/origin-trials
86:03.76 js/src/gc
86:27.53 layout/style
86:53.68 media/libdav1d
87:38.55 netwerk/base
87:41.32 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsURLHelperOSX.cpp:40:15: warning: 'FSGetVolumeInfo' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
87:41.32    40 |       err = ::FSGetVolumeInfo(0, volumeIndex, nullptr, kFSVolInfoNone, nullptr,
87:41.32       |               ^
87:41.32 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:3936:15: note: 'FSGetVolumeInfo' has been explicitly marked deprecated here
87:41.32  3936 | extern OSErr  FSGetVolumeInfo(FSVolumeRefNum volume, ItemCount volumeIndex, FSVolumeRefNum *actualVolume, FSVolumeInfoBitmap whichInfo, FSVolumeInfo *info, HFSUniStr255 *volumeName, FSRef *rootDirectory) __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
87:41.32       |               ^
87:41.33 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsURLHelperOSX.cpp:86:51: warning: 'kCFURLHFSPathStyle' is deprecated: first deprecated in macOS 10.9 - Carbon File Manager is deprecated, use kCFURLPOSIXPathStyle where possible [-Wdeprecated-declarations]
87:41.33    86 |                                                   kCFURLHFSPathStyle, true);
87:41.33       |                                                   ^
87:41.33 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreFoundation.framework/Headers/CFURL.h:23:5: note: 'kCFURLHFSPathStyle' has been explicitly marked deprecated here
87:41.33    23 |     kCFURLHFSPathStyle API_DEPRECATED("Carbon File Manager is deprecated, use kCFURLPOSIXPathStyle where possible", macos(10.0,10.9), ios(2.0,7.0), watchos(2.0,2.0), tvos(9.0,9.0)), /* The use of kCFURLHFSPathStyle is deprecated. The Carbon File Manager, which uses HFS style paths, is deprecated. HFS style paths are unreliable because they can arbitrarily refer to multiple volumes if those volumes have identical volume names. You should instead use kCFURLPOSIXPathStyle wherever possible. */
87:41.33       |     ^
87:41.35 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/netwerk/base/nsURLHelperOSX.cpp:167:13: warning: 'FSPathMakeRef' is deprecated: first deprecated in macOS 10.8 [-Wdeprecated-declarations]
87:41.35   167 |       if (::FSPathMakeRef((UInt8*)possibleVolName.get(), &testRef, nullptr) !=
87:41.35       |             ^
87:41.35 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/System/Library/Frameworks/CoreServices.framework/Frameworks/CarbonCore.framework/Headers/Files.h:4115:18: note: 'FSPathMakeRef' has been explicitly marked deprecated here
87:41.35  4115 | extern OSStatus  FSPathMakeRef(const UInt8 *path, FSRef *ref, Boolean *isDirectory)        __OSX_AVAILABLE_BUT_DEPRECATED(__MAC_10_0, __MAC_10_8, __IPHONE_NA, __IPHONE_NA);
87:41.35       |                  ^
87:41.98 3 warnings generated.
87:56.73 netwerk/dns
89:13.30 security/manager/ssl
89:38.61 toolkit/components/telemetry
89:50.11 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
89:50.11 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
89:50.11 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:91:11: error: redefinition of 'end' with a different type: 'char *' vs 'size_t' (aka 'unsigned long')
89:50.11    91 |     char* end = nullptr;
89:50.11       |           ^
89:50.11 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:83:12: note: previous definition is here
89:50.11    83 |     size_t end = token.find_last_not_of(" \t");
89:50.11       |            ^
89:50.11 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:92:53: error: cannot initialize a parameter of type 'char **' with an rvalue of type 'size_t *' (aka 'unsigned long *')
89:50.11    92 |     unsigned long val = std::strtoul(token.c_str(), &end, 16);
89:50.11       |                                                     ^~~~
89:50.11 /home/runner/.mozbuild/osxcross/target/SDK/MacOSX14.4.sdk/usr/include/stdlib.h:175:37: note: passing argument to parameter '__endptr' here
89:50.11   175 |          strtoul(const char *__str, char **__endptr, int __base);
89:50.11       |                                            ^
89:50.11 In file included from Unified_cpp_security_manager_ssl2.cpp:29:
89:50.11 In file included from /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/security/manager/ssl/nsNSSComponent.cpp:10:
89:50.11 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:27: error: comparison between pointer and integer ('size_t' (aka 'unsigned long') and 'const value_type *' (aka 'const char *'))
89:50.11    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
89:50.11       |                       ~~~ ^  ~~~~~~~~~~~~~
89:50.11 /home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/camoucfg/CamouTLSOverride.hpp:93:47: error: indirection requires pointer operand ('size_t' (aka 'unsigned long') invalid)
89:50.11    93 |     if (errno == 0 && end != token.c_str() && *end == '\0' &&
89:50.11       |                                               ^~~~
89:56.97 toolkit/library/buildid.cpp.stub
89:57.18 toolkit/library
90:01.35 4 errors generated.
90:01.42 gmake[5]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:674: Unified_cpp_security_manager_ssl2.o] Error 1
90:01.42 gmake[4]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:72: security/manager/ssl/target-objects] Error 2
90:01.42 gmake[4]: *** Waiting for unfinished jobs....
91:49.98 gmake[3]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/recurse.mk:34: compile] Error 2
91:50.03 gmake[2]: *** [/home/runner/work/firefox/firefox/camoufox-135.0.1-beta.24/config/rules.mk:359: default] Error 2
91:50.06 gmake[1]: *** [client.mk:60: build] Error 2
91:50.17 W 1029 compiler warnings present.
91:51.85 W Notification center failed: Install notify-send (usually part of the libnotify package) to get a notification when the build finishes.
 Config object not found by mach.
Configure complete!
Be sure to run |mach build| to pick up any changes
  Parallelism determined by memory: using 4 jobs for 4 cores based on 15.6 GiB RAM and estimated job size of 1.0 GiB
make: *** [Makefile:132: build] Error 2

------------
make set-target
------------


------------
make build
------------

fatal error: command 'make build' failed
Error: Process completed with exit code 1.