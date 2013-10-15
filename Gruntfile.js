module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        jshint: {
            all:['src/pokeradio/public/js/*.js']
        },
        less: {
            development: {
                options: {
                    paths: ["src/pokeradio/public/css"]
                },
                files: {
                    "src/pokeradio/public/css/main.css": "src/pokeradio/public/css/less/main.less"
                }
            },
            production: {
                options: {
                    paths: ["src/pokeradio/public/css"],
                    yuicompress: true
                },
                files: {
                    "src/pokeradio/public/css/main.css": "src/pokeradio/public/css/less/main.less"
                }
            }
        },
        watch: {
            files: ["src/pokeradio/public/css/less/*.less"],
            tasks: ['less:development'],
            css: {
                files: ["src/pokeradio/public/css/*.css"],
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