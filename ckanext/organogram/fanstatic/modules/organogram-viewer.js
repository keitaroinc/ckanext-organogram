/*
Copyright (c) 2018 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

ckan.module('organogram-viewer', function ($, _) {
  function showError() {
    $('[data-module=organogram-viewer]').append('<div class="organogram-error"><span class="empty">' + _('Sorry, organogram data is currently unavailable.').fetch() + '</span></div>');
  }
  return {
    initialize: function () {
      $.ajax({
        url: window.location.origin + "/api/action/config_option_show?key=ckanext.organogram.file_url",
        dataType: 'json',
        success: function (response) {
          var organogram_file_url = response.result
          if (organogram_file_url.indexOf('http://') === -1 && organogram_file_url.indexOf('https://') === -1) {
            organogram_url = window.location.origin + '/uploads/organogram/' + organogram_file_url
            $.ajax({
              url: organogram_url,
              dataType: 'json',
              success: function (_result) {
                showOrganogram(_result)
              },
              error: function () {
                showError();
              }
            })
          } else {
            $.ajax({
              url: organogram_file_url,
              dataType: 'json',
              success: function (_result) {
                showOrganogram(_result)
              }
            })
          }
        }
      });

      function showOrganogram(json) {
        //Create a new ST instance
        var st = new $jit.ST({
          //id of viz container element
          injectInto: 'infovis',
          //set duration for the animation
          duration: 200,
          //set animation transition type
          transition: $jit.Trans.Quart.easeInOut,
          //set distance between node and its children
          levelDistance: 50,
          //enable panning
          Navigation: {
            enable: true,
            panning: true
          },
          //set node and edge styles
          //set overridable=true for styling individual
          //nodes or edges
          Node: {
            height: 80,
            width: 130,
            type: 'rectangle',
            color: '#ddd',
            overridable: true
          },

          Edge: {
            type: 'bezier',
            overridable: true
          },

          //This method is called on DOM label creation.
          //Use this method to add event handlers and styles to
          //your node.
          onCreateLabel: function (label, node) {
            label.id = node.id;
            label.innerHTML = node.name;
            label.onclick = function () {
              st.onClick(node.id);
            };
            //set label styles
            var style = label.style;
            style.width = 80 + 'px';
            style.height = 50 + 'px';
            style.cursor = 'pointer';
            style.color = '#222';
            style.fontSize = '1rem';
            style.textAlign = 'center';
            style.paddingTop = '5px';
          },

          //This method is called right before plotting
          //a node. It's useful for changing an individual node
          //style properties before plotting it.
          //The data properties prefixed with a dollar
          //sign will override the global node style properties.
          onBeforePlotNode: function (node) {
            //add some color to the nodes in the path between the
            //root node and the selected node.
            if (node.selected) {
              node.data.$color = "#EEFF8A";
            } else {
              delete node.data.$color;
              //if the node belongs to the last plotted level
              if (!node.anySubnode("exist")) {
                //count children number
                var count = 0;
                node.eachSubnode(function (n) {
                  count++;
                });
                //assign a node color based on
                //how many children it has
                node.data.$color = ['#c8cbd3', '#b1b6c2', '#aebdda', '#95c8ca', '#c1b8db', '#d6bca0'][count];
              }
            }
          },

          //This method is called right before plotting
          //an edge. It's useful for changing an individual edge
          //style properties before plotting it.
          //Edge data proprties prefixed with a dollar sign will
          //override the Edge global style properties.
          onBeforePlotLine: function (adj) {
            if (adj.nodeFrom.selected && adj.nodeTo.selected) {
              adj.data.$color = "#46aeb0";
              adj.data.$lineWidth = 3;
            } else {
              delete adj.data.$color;
              delete adj.data.$lineWidth;
            }
          }
        });
        //load json data
        st.loadJSON(json);
        //compute node positions and layout
        st.compute();
        //optional: make a translation of the tree
        st.geom.translate(new $jit.Complex(-200, 0), "current");
        //emulate a click on the root node.
        st.onClick(st.root);
      }
    }
  }
})
