from fanstatic import Library, Resource

library = Library('lodash', 'resources')

lodash = Resource(
    library, 'js/lodash.js',
    minified='js/lodash.min.js'
)

lodash_core = Resource(
    library, 'js/lodash.core.js',
    minified='js/lodash.core.min.js'
)
