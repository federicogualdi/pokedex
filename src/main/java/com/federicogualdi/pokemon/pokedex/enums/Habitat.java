package com.federicogualdi.pokemon.pokedex.enums;

public enum Habitat {

    CAVE("cave");

    private final String value;

    Habitat(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

}
