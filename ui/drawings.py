import PySimpleGUI as Sg

measurement_graph = Sg.Graph(canvas_size=(400, 100),
                             graph_bottom_left=(0, 0),
                             graph_top_right=(400, 100),
                             key='__GRAPH__',
                             border_width=10
                             )


def draw_the_things(graph: Sg.Graph):
    rect1 = graph.draw_rectangle(top_left=(25, 75),
                                 bottom_right=(75, 25),
                                 line_color="white",
                                 fill_color='grey',
                                 )
    rect2 = graph.draw_rectangle(top_left=(325, 75),
                                 bottom_right=(375, 25),
                                 line_color="white",
                                 fill_color='grey',
                                 )
    circ1 = graph.draw_circle(center_location=(150, 50),
                              radius=25,
                              line_color="white",
                              fill_color='grey',
                              )
    circ2 = graph.draw_circle(center_location=(250, 50),
                              radius=25,
                              line_color="white",
                              fill_color='grey',
                              )
    text1 = graph.draw_text(text='L1',
                            location=(50, 50),
                            font=10,
                            color='black',
                            )
    text2 = graph.draw_text(text='L2',
                            location=(350, 50),
                            font=10,
                            color='black',
                            )

    rectangles = [rect1, rect2]
    circles = [circ1, circ2]
    texts = [text1, text2]
    return graph, rectangles, circles, texts
