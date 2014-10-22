module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            all:['pokeradio/public/js/*.js']
        },
        less: {
            development: {
                options: {
                    paths: ["pokeradio/public/css"]
                },
                files: {
                    "pokeradio/public/css/main.css": "pokeradio/public/less/main.less",
                     "pokeradio/public/css/bootstrap.css": "pokeradio/public/less/bootstrap/bootstrap.less"

                }
            },
            production: {
                options: {
                    paths: ["pokeradio/public/css"],
                    yuicompress: true
                },
                files: {
                    "pokeradio/public/css/main.css": "pokeradio/public/less/main.less"
                }
            }
        },
        watch: {
            files: ["pokeradio/public/less/*.less",
                    "pokeradio/public/less/*/*.less",
                    "pokeradio/public/less/bootstrap/*.less"],
            tasks: ['less:development'],
            css: {
                files: ["pokeradio/public/css/*.css"],
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
