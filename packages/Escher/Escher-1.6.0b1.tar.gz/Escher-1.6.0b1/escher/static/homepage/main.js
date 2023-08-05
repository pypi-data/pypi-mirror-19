/* global d3 */

var MAP_DOWNLOAD, SERVER_INDEX, LOCAL_INDEX

/**
 * Get model from a map name.
 */
function get_model(name) {
  var parts = name.split('.')
  if (parts.length == 2)
    return parts[0]
  return null
}

function select_model(model_name) {
  var sel = d3.select('#models'),
      ind = 0
  sel.selectAll('option')
    .each(function(d, i) {
      if (d && (d.model_name == model_name))
        ind = i
    })
  sel.node().selectedIndex = ind
}

/**
 * Find maps with the same model. Returns null if no quick jump options could be
 * found.
 */
function get_quick_jump(this_map, server_index, local_index) {
  var model = get_model(this_map)
  if (model === null)
    return null

  var quick_jump = {},
      all_maps = []
  if (server_index !== null)
    all_maps = all_maps.concat(server_index.maps)
  if (local_index !== null)
    all_maps = all_maps.concat(local_index.maps)
  all_maps.forEach(function(o) {
    if (get_model(o.map_name) == model)
      quick_jump[o.map_name] = true
  })
  quick_jump = Object.keys(quick_jump)
  return quick_jump.length == 0 ? null : quick_jump
}

function submit(server_index, local_index, map_download) {
  // get the selections
  var maps = d3.select('#maps'),
      map_data = (maps.selectAll('option')
                  .filter(function(d, i) {
                    return i == maps.node().selectedIndex
                  }).node().__data__),
      map_name = map_data ? map_data.map_name : null,
      organism = map_data ? map_data.organism : null,
      model_name = d3.select('#models').node().value,
      options_value = d3.select('#tools').node().value,
      scroll_value = d3.select('#scroll').node().checked,
      never_ask_value = d3.select('#never_ask').node().checked,
      add = [],
      url
  // only add model for builder
  if (model_name != 'none' && options_value == 'builder')
    add.push('model_name=' + model_name)
  if (map_name !== null)
    add.push('map_name=' + map_name)
  if (scroll_value)
    add.push('scroll_behavior=zoom')
  if (never_ask_value)
    add.push('never_ask_before_quit=true')
  if (options_value == 'viewer')
    add.push('enable_editing=false')
  else
    add.push('enable_editing=true')

  // choose the file
  url = 'builder/index.html'
  add.push('js_source=local')

  // set the quick jump maps
  if (map_name) {
    var quick_jump = get_quick_jump(map_name, server_index, local_index)
    if (quick_jump !== null) {
      quick_jump.forEach(function(o) {
        add.push('quick_jump[]=' + o)
      })
      add.push('quick_jump_path=' + map_download + encodeURIComponent(organism))
    }
  }

  url += '?'
  for (var i=0, l=add.length; i < l; i++) {
    if (i > 0) url += '&'
    url += add[i]
  }
  window.open(url,'_blank')
}

/**
 * Draw the models selector.
 */
function draw_models_select(server_index, local_index) {
  // filter function
  var filter_models = function(d) {
    var org = d3.select('#organisms').node().value
    if (org =='all')
      return true
    if (org == d.organism)
      return true
    return false
  }

  var web_sel, local_sel,
      select_sel = d3.select('#models')
  if (local_index === null) {
    // no cache
    web_sel = select_sel
  } else {
    // local cache
    select_sel.selectAll('optgroup')
      .data([['local', 'Cached'], ['web', 'Web']])
      .enter()
      .append('optgroup')
      .attr('label', function(d) { return d[1]; })
      .attr('id', function(d) { return 'models-' + d[0]; })
    web_sel = select_sel.select('#models-web')
    local_sel = select_sel.select('#models-local')
  }

  // cached
  var local_model_names = [], model_data, map_data
  if (local_index !== null) {
    model_data = local_index.models.filter(filter_models)
    local_model_names = model_data.map(function(x) { return x.model_name; })

    var models_sel = local_sel.selectAll('.model')
          .data(model_data, function(d) { return d.model_name; })
    models_sel.enter()
      .append('option')
      .classed('model', true)
    models_sel.attr('value', function(d) { return d.model_name; })
      .text(function(d) {
        var parts = d.model_name.split('.')
        if (parts.length==2) {
          return d.model_name.split('.').slice(-1)[0]
        } else {
          return d.model_name
        }
      })
    models_sel.exit().remove()
  }

  // web
  if (server_index !== null) {
    model_data = server_index.models
      .filter(filter_models)
      .filter(function(o) { return local_model_names.indexOf(o.model_name) == -1; })
    models_sel = web_sel.selectAll('.model')
      .data(model_data, function(d) { return d.model_name; })
    models_sel.enter()
      .append('option')
      .classed('model', true)
    models_sel.attr('value', function(d) { return d.model_name; })
      .text(function(d) {
        return d.model_name.split('.').slice(-1)[0]
      })
    models_sel.exit().remove()
  }

}

/**
 * Draw the models selector.
 * @param {Object} server_index - The index for the server.
 * @param {Object} local_index - The index of local maps and models
 * @return {Boolean} True if there are maps, and false if no maps.
 */
function draw_maps_select(server_index, local_index) {
  var filter_maps = function(d) {
    var org = d3.select('#organisms').node().value
    if (org == 'all')
      return true
    if (org == d.organism)
      return true
    return false
  }

  var select_sel = d3.select('#maps')
  if (local_index === null) {
    // no cache
    web_sel = select_sel
  } else {
    // local cache
    select_sel.selectAll('optgroup')
      .data([['local', 'Cached'], ['web', 'Web']])
      .enter()
      .append('optgroup')
      .attr('label', function(d) { return d[1]; })
      .attr('id', function(d) { return 'maps-' + d[0]; })
    var web_sel = d3.select('#maps-web'),
        local_sel = d3.select('#maps-local')
  }

  // cached
  var local_map_names = [],
      has_maps = false,
      map_data
  if (local_index !== null) {
    map_data = local_index.maps.filter(filter_maps)
    local_map_names = map_data.map(function(x) { return x.map_name; })
    if (map_data.length > 0)
      has_maps = true

    var maps_sel = local_sel.selectAll('.map')
          .data(map_data, function(d) { return d.map_name; })
    maps_sel.enter()
      .append('option')
      .classed('map', true)
    maps_sel
      .text(function(d) {
        var parts = d.map_name.split('.')
        if (parts.length == 2) {
          var map = d.map_name.split('.').slice(-1)[0],
              model = get_model(d.map_name)
          return map + ' (' + model + ')'
        } else {
          return d.map_name
        }
      })
    maps_sel.exit().remove()
  }

  // web
  if (server_index !== null) {
    map_data = server_index.maps
      .filter(filter_maps)
      .filter(function(o) { return local_map_names.indexOf(o.map_name) == -1; })
    if (map_data.length > 0)
      has_maps = true

    maps_sel = web_sel.selectAll('.map')
      .data(map_data, function(d) { return d.map_name; })
    maps_sel.enter()
      .append('option')
      .classed('map', true)
    maps_sel
      .text(function(d) {
        var map = d.map_name.split('.').slice(-1)[0],
            model = get_model(d.map_name)
        return map + ' (' + model + ')'
      })
    maps_sel.exit().remove()
  }

  // select the first map and model
  if (has_maps && select_sel.node().selectedIndex == 0) {
    select_sel.node().selectedIndex = 1
    select_sel
      .selectAll('option')
      .each(function(d, i) {
        if (i == 1) select_model(get_model(d.map_name))
      })
  }

  return has_maps
}

function draw_organisms_select(organisms) {
  var org = d3.select('#organisms').selectAll('.organism')
        .data(organisms, function(d) { return d; })
  org.enter()
    .append('option')
    .classed('organism', true)
  org.attr('value', function(d) { return d; })
    .text(function(d) { return d; })
}

function setup(server_index, local_index, map_download) {
  // GO
  var uniq = function(a) {
    var seen = {}
    return a.filter(function(item) {
      return seen.hasOwnProperty(item) ? false : (seen[item] = true)
    })
  }
  var not_cached = function(web, local) {
    if (local === null) return web
    return web.filter(function(m) {
      return local.indexOf(m) == -1
    })
  }

  // organisms
  var organisms = {}
  ;[local_index, server_index]
    .filter(function(x) { return x !== null; })
    .forEach(function(i) {
      ;['maps', 'models'].forEach(function(n) {
        i[n].forEach(function(m) {
          organisms[m.organism] = true
        })
      })
    })
  organisms = Object.keys(organisms)

  // draw dropdown menus
  draw_organisms_select(organisms)
  draw_models_select(server_index, local_index)
  var has_maps = draw_maps_select(server_index, local_index)

  // update filters
  d3.select('#organisms')
    .on('change', function() {
      draw_models_select(server_index, local_index)
      draw_maps_select(server_index, local_index)
    })

  // select an appropriate model for selected map
  d3.select('#maps')
    .on('change', function() {
      var is_none = this.value == 'none'
      var selectedIndex = this.selectedIndex
      d3.select(this)
        .selectAll('option')
        .each(function(d, i) {
          if (d && i == selectedIndex)
            select_model(get_model(d.map_name))
        })
    })

  // disable Model for viewer
  d3.select('#tools')
    .on('change', function() {
      d3.select('#models')
        .attr('disabled', this.value.indexOf('viewer') == -1 ? null : true)
    })

  // select the first map
  var map_node = d3.select('#maps').node()
  if (has_maps && map_node.selectedIndex == 0)
    map_node.selectedIndex = 1

  // submit button
  d3.select('#submit')
    .on('click', submit.bind(null, server_index, local_index, map_download))

  // submit on enter
  var selection = d3.select(window),
      kc = 13
  selection.on('keydown.'+kc, function() {
    if (d3.event.keyCode==kc) {
      submit(server_index, local_index, map_download)
    }
  })
}
