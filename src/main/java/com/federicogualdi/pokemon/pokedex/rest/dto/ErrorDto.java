package com.federicogualdi.pokemon.pokedex.rest.dto;

public class ErrorDto {

    private String title;
    private Integer status;

    private String detail;

    public ErrorDto title(String title) {
        this.title = title;
        return this;
    }

    public String getTitle() {
        return title;
    }

    public ErrorDto status(Integer status) {
        this.status = status;
        return this;
    }

    public Integer getStatus() {
        return status;
    }

    public void setDetail(String detail) {
        this.detail = detail;
    }

    public String getDetail() {
        return detail;
    }

    @Override
    public String toString() {
        return "ErrorDto{" + "title='" + title + '\'' + ", status=" + status + '}';
    }
}

