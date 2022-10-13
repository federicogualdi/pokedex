package com.federicogualdi.pokemon.pokedex.enums;

public enum Language {

    EN("en");

    private String value;

    Language(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

}
