for bnmfn in artnets/*.bnm; do
    bbnm=`basename $bnmfn .bnm`
    g=`echo $bbnm | cut -d'_' -f2`
    idtdn=artdats/$bbnm
    mkdir -p $idtdn
    vdfn=artdats/data_$g.vd
    echo $bbnm
    for j in `seq 0 99`; do
	idtfn=$idtdn/$j.idt
	python -m bn.model.bn_gendata -o $idtfn $vdfn $bnmfn 1000
    done
done

