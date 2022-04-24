# Multiplex level processing
MULTIPLEXEDGELIST=$1
LAYERS=$(awk '{print $1}' $MULTIPLEXEDGELIST | sort -n | uniq)

# Within each layer, map edges
for l in $LAYERS
do
    # Gather raw edges
    raw=$(grep "^l" $MULTIPLEXEDGELIST)
    src=$(awk '{print $2}' $raw)
    tgt=$(awk '{print $3}' $raw)
    
    # Map sources
    $src > _src
    for node in $(cat $src)
    do
        echo $(grep "^$node," normalize_node_indices.mapping | awk -F, '{print $2}') >> _mapped_src
    done
    rm _src

    # Map targets
    $tgt > _tgt
    for node in $(cat $tgt)
    do
        echo $(grep "^$node," normalize_node_indices.mapping | awk -F, '{print $2}') >> _mapped_tgt
    done
    rm _tgt

    # Concatenate src and tgt
    paste -d " " _mapped_src _mapped_tgt > _mapped_edges 
    rm _mapped_src _mapped_tgt

    # Prepend layer information
    sed -i "s/^/$l " _mapped_edges

    # Save elsewhere so we don't override with next layer
    mv _mapped_edges _mapped_edges_$l
    rm _mapped_edges
done

cat _mapped_edges_* > mapped_$MULTIPLEXEDGELIST
