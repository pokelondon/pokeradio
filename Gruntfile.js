module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            all:['web/pokeradio/public/js/*.js']
        },
        less: {
            development: {
                options: {
                    paths: ["web/pokeradio/public/css"]
                },
                files: {
                    "web/pokeradio/public/css/main.css": "web/pokeradio/public/less/main.less",
                     "web/pokeradio/public/css/bootstrap.css": "web/pokeradio/public/less/bootstrap/bootstrap.less"

                }
            },
            production: {
                options: {
                    paths: ["web/pokeradio/public/css"],
                    yuicompress: true
                },
                files: {
                    "web/pokeradio/public/css/main.css": "web/pokeradio/public/less/main.less"
                }
            }
        },
        watch: {
            files: ["web/pokeradio/public/less/*.less",
                    "web/pokeradio/public/less/*/*.less",
                    "web/pokeradio/public/less/bootstrap/*.less"],
            tasks: ['less:development'],
            css: {
                files: ["web/pokeradio/public/css/*.css"],
                options: {
                    livereload: true,
                }
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');


    // Default task(s).
    grunt.registerTask('default', ['watch']);
    grunt.registerTask('build', ['jshint', 'less']);

};
