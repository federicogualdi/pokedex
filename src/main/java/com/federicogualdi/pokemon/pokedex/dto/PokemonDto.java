package com.federicogualdi.pokemon.pokedex.dto;


public class PokemonDto {
    public String name;
    public String description;
    public String habitat;
    public Boolean isLegendary;

    public PokemonDto() {
    }

    @Override
    public String toString() {
        return "PokemonDto{" + "name='" + name + '\'' + ", description='" + description + '\'' + ", habitat='" + habitat + '\'' + ", isLegendary=" + isLegendary + '}';
    }
}


